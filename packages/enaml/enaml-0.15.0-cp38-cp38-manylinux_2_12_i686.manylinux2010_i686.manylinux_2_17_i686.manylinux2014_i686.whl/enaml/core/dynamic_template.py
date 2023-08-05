#------------------------------------------------------------------------------
# Copyright (c) 2013, Nucleic Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
#------------------------------------------------------------------------------
from atom.api import Dict, List, Str, Tuple, Typed

from enaml.application import ScheduledTask, schedule
from enaml.objectdict import ObjectDict

from .declarative import Declarative, d_, observe
from .template import Template


class Tagged(ObjectDict):
    """ An empty ObjectDict subclass.

    This subclass helps provide more informative error messages by
    having a class name which reflects it's used.

    """
    __slots__ = ()


def make_tagged(items, tags, startag):
    """ Create a Tagged object for the given items.

    Parameters
    ----------
    items : list
        The list of objects which should be tagged.

    tags : tuple
        A tuple of string tag names. This should be an empty tuple if
        no named tags are available.

    startag : str
        The star tag name. This should be an empty string if there is
        no star tag available.

    Returns
    -------
    result : Tagged
        The tagged object for the given items.

    """
    if tags and len(tags) > len(items):
        msg = 'need more than %d values to unpack'
        raise ValueError(msg % len(items))
    if tags and not startag and len(items) > len(tags):
        raise ValueError('too many values to unpack')
    tagged = Tagged()
    if tags:
        for name, item in zip(tags, items):
            tagged[name] = item
    if startag:
        tagged[startag] = tuple(items[len(tags):])
    return tagged


class DynamicTemplate(Declarative):
    """ An object which dynamically instantiates a template.

    A DynamicTemplate allows a template to be instantiated using the
    runtime scope available to RHS expressions.

    Creating a DynamicTemplate without a parent is a programming error.

    """
    #: The template object to instantiate.
    base = d_(Typed(Template))

    #: The arguments to pass to the template.
    args = d_(Tuple())

    #: The tags to apply to the return values of the template. The tags
    #: are used as the key names for the 'tagged' ObjectDict.
    tags = d_(Tuple(Str()))

    #: The tag to apply to overflow return items from the template.
    startag = d_(Str())

    #: The data keywords to apply to the instantiated items.
    data = d_(Dict())

    #: The object dictionary which maps tag name to tagged object. This
    #: is updated automatically when the template is instantiated.
    tagged = Typed(ObjectDict, ())

    #: The internal task used to collapse template updates.
    _update_task = Typed(ScheduledTask)

    #: The internal list of items generated by the template.
    _items = List(Declarative)

    def initialize(self):
        """ A reimplemented initializer.

        This method will instantiate the template and initialize the
        items for the first time.

        """
        self._refresh()
        for item in self._items:
            item.initialize()
        super(DynamicTemplate, self).initialize()

    def destroy(self):
        """ A reimplemented destructor.

        This method will ensure that the instantiated tempalte items are
        destroyed and that any potential reference cycles are released.

        """
        parent = self.parent
        destroy_items = parent is None or not parent.is_destroyed
        super(DynamicTemplate, self).destroy()
        if destroy_items:
            for item in self._items:
                if not item.is_destroyed:
                    item.destroy()
        del self.data
        del self.tagged
        if self._update_task is not None:
            self._update_task.unschedule()
            del self._update_task
        del self._items

    #--------------------------------------------------------------------------
    # Private API
    #--------------------------------------------------------------------------
    @observe('base', 'args', 'tags', 'startag', 'data')
    def _schedule_refresh(self, change):
        """ Schedule an item refresh when the item dependencies change.

        """
        if change['type'] == 'update':
            if self._update_task is None:
                self._update_task = schedule(self._refresh)

    def _refresh(self):
        """ Refresh the template instantiation.

        This method will destroy the old items, build the new items,
        and then update the parent object and tagged object.

        """
        self._update_task = None

        if self.base is not None:
            items = self.base(*self.args)(**self.data)
        else:
            items = []

        for old in self._items:
            if not old.is_destroyed:
                old.destroy()

        if len(items) > 0:
            self.parent.insert_children(self, items)

        self._items = items
        self.tagged = make_tagged(items, self.tags, self.startag)
