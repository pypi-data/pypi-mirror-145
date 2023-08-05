#------------------------------------------------------------------------------
# Copyright (c) 2013-2017, Nucleic Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
#------------------------------------------------------------------------------
#: A static mapping of language theme token name to lexer attribute name.
TOKENS = {
    "bash": {
        "backticks": "Backticks",
        "comment": "Comment",
        "default": "Default",
        "double_quoted_string": "DoubleQuotedString",
        "error": "Error",
        "here_document_delimiter": "HereDocumentDelimiter",
        "identifier": "Identifier",
        "keyword": "Keyword",
        "number": "Number",
        "operator": "Operator",
        "parameter_expansion": "ParameterExpansion",
        "scalar": "Scalar",
        "single_quoted_here_document": "SingleQuotedHereDocument",
        "single_quoted_string": "SingleQuotedString"
    },
    "batch": {
        "comment": "Comment",
        "default": "Default",
        "external_command": "ExternalCommand",
        "hide_command_char": "HideCommandChar",
        "keyword": "Keyword",
        "label": "Label",
        "operator": "Operator",
        "variable": "Variable"
    },
    "cmake": {
        "block_foreach": "BlockForeach",
        "block_if": "BlockIf",
        "block_macro": "BlockMacro",
        "block_while": "BlockWhile",
        "comment": "Comment",
        "default": "Default",
        "function": "Function",
        "keyword_set3": "KeywordSet3",
        "label": "Label",
        "number": "Number",
        "string": "String",
        "string_left_quote": "StringLeftQuote",
        "string_right_quote": "StringRightQuote",
        "string_variable": "StringVariable",
        "variable": "Variable"
    },
    "cpp": {
        "comment": "Comment",
        "comment_doc": "CommentDoc",
        "comment_doc_keyword": "CommentDocKeyword",
        "comment_doc_keyword_error": "CommentDocKeywordError",
        "comment_line": "CommentLine",
        "comment_line_doc": "CommentLineDoc",
        "default": "Default",
        "double_quoted_string": "DoubleQuotedString",
        "global_class": "GlobalClass",
        "hash_quoted_string": "HashQuotedString",
        "identifier": "Identifier",
        "inactive_comment": "InactiveComment",
        "inactive_comment_doc": "InactiveCommentDoc",
        "inactive_comment_doc_keyword": "InactiveCommentDocKeyword",
        "inactive_comment_doc_keyword_error": "InactiveCommentDocKeywordError",
        "inactive_comment_line": "InactiveCommentLine",
        "inactive_comment_line_doc": "InactiveCommentLineDoc",
        "inactive_default": "InactiveDefault",
        "inactive_double_quoted_string": "InactiveDoubleQuotedString",
        "inactive_global_class": "InactiveGlobalClass",
        "inactive_hash_quoted_string": "InactiveHashQuotedString",
        "inactive_identifier": "InactiveIdentifier",
        "inactive_keyword": "InactiveKeyword",
        "inactive_keyword_set2": "InactiveKeywordSet2",
        "inactive_number": "InactiveNumber",
        "inactive_operator": "InactiveOperator",
        "inactive_pre_processor": "InactivePreProcessor",
        "inactive_pre_processor_comment": "InactivePreProcessorComment",
        "inactive_raw_string": "InactiveRawString",
        "inactive_regex": "InactiveRegex",
        "inactive_single_quoted_string": "InactiveSingleQuotedString",
        "inactive_triple_quoted_verbatim_string": "InactiveTripleQuotedVerbatimString",
        "inactive_unclosed_string": "InactiveUnclosedString",
        "inactive_uuid": "InactiveUUID",
        "inactive_verbatim_string": "InactiveVerbatimString",
        "keyword": "Keyword",
        "keyword_set2": "KeywordSet2",
        "number": "Number",
        "operator": "Operator",
        "pre_processor": "PreProcessor",
        "pre_processor_comment": "PreProcessorComment",
        "raw_string": "RawString",
        "regex": "Regex",
        "single_quoted_string": "SingleQuotedString",
        "triple_quoted_verbatim_string": "TripleQuotedVerbatimString",
        "unclosed_string": "UnclosedString",
        "uuid": "UUID",
        "verbatim_string": "VerbatimString"
    },
    "csharp": {
        # this uses the "cpp" token set
    },
    "css": {
        "at_rule": "AtRule",
        "attribute": "Attribute",
        "class_selector": "ClassSelector",
        "comment": "Comment",
        "css1_property": "CSS1Property",
        "css2_property": "CSS2Property",
        "css3_property": "CSS3Property",
        "default": "Default",
        "double_quoted_string": "DoubleQuotedString",
        "extended_css_property": "ExtendedCSSProperty",
        "extended_pseudo_class": "ExtendedPseudoClass",
        "extended_pseudo_element": "ExtendedPseudoElement",
        "id_selector": "IDSelector",
        "important": "Important",
        "media_rule": "MediaRule",
        "operator": "Operator",
        "pseudo_class": "PseudoClass",
        "pseudo_element": "PseudoElement",
        "single_quoted_string": "SingleQuotedString",
        "tag": "Tag",
        "unknown_property": "UnknownProperty",
        "unknown_pseudo_class": "UnknownPseudoClass",
        "value": "Value",
        "variable": "Variable"
    },
    "d": {
        "backquote_string": "BackquoteString",
        "character": "Character",
        "comment": "Comment",
        "comment_doc": "CommentDoc",
        "comment_doc_keyword": "CommentDocKeyword",
        "comment_doc_keyword_error": "CommentDocKeywordError",
        "comment_line": "CommentLine",
        "comment_line_doc": "CommentLineDoc",
        "comment_nested": "CommentNested",
        "default": "Default",
        "identifier": "Identifier",
        "keyword": "Keyword",
        "keyword_doc": "KeywordDoc",
        "keyword_secondary": "KeywordSecondary",
        "keyword_set5": "KeywordSet5",
        "keyword_set6": "KeywordSet6",
        "keyword_set7": "KeywordSet7",
        "number": "Number",
        "operator": "Operator",
        "raw_string": "RawString",
        "string": "String",
        "typedefs": "Typedefs",
        "unclosed_string": "UnclosedString"
    },
    "diff": {
        "command": "Command",
        "comment": "Comment",
        "default": "Default",
        "header": "Header",
        "line_added": "LineAdded",
        "line_changed": "LineChanged",
        "line_removed": "LineRemoved",
        "position": "Position"
    },
    "enaml": {
        # this uses the "python" token set
    },
    "fortran": {
        # this uses the "fortran77" token set
    },
    "fortran77": {
        "comment": "Comment",
        "continuation": "Continuation",
        "default": "Default",
        "dotted_operator": "DottedOperator",
        "double_quoted_string": "DoubleQuotedString",
        "extended_function": "ExtendedFunction",
        "identifier": "Identifier",
        "intrinsic_function": "IntrinsicFunction",
        "keyword": "Keyword",
        "label": "Label",
        "number": "Number",
        "operator": "Operator",
        "pre_processor": "PreProcessor",
        "single_quoted_string": "SingleQuotedString",
        "unclosed_string": "UnclosedString"
    },
    "html": {
        "asp_at_start": "ASPAtStart",
        "asp_java_script_comment": "ASPJavaScriptComment",
        "asp_java_script_comment_doc": "ASPJavaScriptCommentDoc",
        "asp_java_script_comment_line": "ASPJavaScriptCommentLine",
        "asp_java_script_default": "ASPJavaScriptDefault",
        "asp_java_script_double_quoted_string": "ASPJavaScriptDoubleQuotedString",
        "asp_java_script_keyword": "ASPJavaScriptKeyword",
        "asp_java_script_number": "ASPJavaScriptNumber",
        "asp_java_script_regex": "ASPJavaScriptRegex",
        "asp_java_script_single_quoted_string": "ASPJavaScriptSingleQuotedString",
        "asp_java_script_start": "ASPJavaScriptStart",
        "asp_java_script_symbol": "ASPJavaScriptSymbol",
        "asp_java_script_unclosed_string": "ASPJavaScriptUnclosedString",
        "asp_java_script_word": "ASPJavaScriptWord",
        "asp_python_class_name": "ASPPythonClassName",
        "asp_python_comment": "ASPPythonComment",
        "asp_python_default": "ASPPythonDefault",
        "asp_python_double_quoted_string": "ASPPythonDoubleQuotedString",
        "asp_python_function_method_name": "ASPPythonFunctionMethodName",
        "asp_python_identifier": "ASPPythonIdentifier",
        "asp_python_keyword": "ASPPythonKeyword",
        "asp_python_number": "ASPPythonNumber",
        "asp_python_operator": "ASPPythonOperator",
        "asp_python_single_quoted_string": "ASPPythonSingleQuotedString",
        "asp_python_start": "ASPPythonStart",
        "asp_python_triple_double_quoted_string": "ASPPythonTripleDoubleQuotedString",
        "asp_python_triple_single_quoted_string": "ASPPythonTripleSingleQuotedString",
        "asp_start": "ASPStart",
        "aspvb_script_comment": "ASPVBScriptComment",
        "aspvb_script_default": "ASPVBScriptDefault",
        "aspvb_script_identifier": "ASPVBScriptIdentifier",
        "aspvb_script_keyword": "ASPVBScriptKeyword",
        "aspvb_script_number": "ASPVBScriptNumber",
        "aspvb_script_start": "ASPVBScriptStart",
        "aspvb_script_string": "ASPVBScriptString",
        "aspvb_script_unclosed_string": "ASPVBScriptUnclosedString",
        "aspxc_comment": "ASPXCComment",
        "attribute": "Attribute",
        "cdata": "CDATA",
        "default": "Default",
        "entity": "Entity",
        "html_comment": "HTMLComment",
        "html_double_quoted_string": "HTMLDoubleQuotedString",
        "html_number": "HTMLNumber",
        "html_single_quoted_string": "HTMLSingleQuotedString",
        "html_value": "HTMLValue",
        "java_script_comment": "JavaScriptComment",
        "java_script_comment_doc": "JavaScriptCommentDoc",
        "java_script_comment_line": "JavaScriptCommentLine",
        "java_script_default": "JavaScriptDefault",
        "java_script_double_quoted_string": "JavaScriptDoubleQuotedString",
        "java_script_keyword": "JavaScriptKeyword",
        "java_script_number": "JavaScriptNumber",
        "java_script_regex": "JavaScriptRegex",
        "java_script_single_quoted_string": "JavaScriptSingleQuotedString",
        "java_script_start": "JavaScriptStart",
        "java_script_symbol": "JavaScriptSymbol",
        "java_script_unclosed_string": "JavaScriptUnclosedString",
        "java_script_word": "JavaScriptWord",
        "other_in_tag": "OtherInTag",
        "php_comment": "PHPComment",
        "php_comment_line": "PHPCommentLine",
        "php_default": "PHPDefault",
        "php_double_quoted_string": "PHPDoubleQuotedString",
        "php_double_quoted_variable": "PHPDoubleQuotedVariable",
        "php_keyword": "PHPKeyword",
        "php_number": "PHPNumber",
        "php_operator": "PHPOperator",
        "php_single_quoted_string": "PHPSingleQuotedString",
        "php_start": "PHPStart",
        "php_variable": "PHPVariable",
        "python_class_name": "PythonClassName",
        "python_comment": "PythonComment",
        "python_default": "PythonDefault",
        "python_double_quoted_string": "PythonDoubleQuotedString",
        "python_function_method_name": "PythonFunctionMethodName",
        "python_identifier": "PythonIdentifier",
        "python_keyword": "PythonKeyword",
        "python_number": "PythonNumber",
        "python_operator": "PythonOperator",
        "python_single_quoted_string": "PythonSingleQuotedString",
        "python_start": "PythonStart",
        "python_triple_double_quoted_string": "PythonTripleDoubleQuotedString",
        "python_triple_single_quoted_string": "PythonTripleSingleQuotedString",
        "script": "Script",
        "sgml_block_default": "SGMLBlockDefault",
        "sgml_command": "SGMLCommand",
        "sgml_comment": "SGMLComment",
        "sgml_default": "SGMLDefault",
        "sgml_double_quoted_string": "SGMLDoubleQuotedString",
        "sgml_entity": "SGMLEntity",
        "sgml_error": "SGMLError",
        "sgml_parameter": "SGMLParameter",
        "sgml_parameter_comment": "SGMLParameterComment",
        "sgml_single_quoted_string": "SGMLSingleQuotedString",
        "sgml_special": "SGMLSpecial",
        "tag": "Tag",
        "unknown_attribute": "UnknownAttribute",
        "unknown_tag": "UnknownTag",
        "vb_script_comment": "VBScriptComment",
        "vb_script_default": "VBScriptDefault",
        "vb_script_identifier": "VBScriptIdentifier",
        "vb_script_keyword": "VBScriptKeyword",
        "vb_script_number": "VBScriptNumber",
        "vb_script_start": "VBScriptStart",
        "vb_script_string": "VBScriptString",
        "vb_script_unclosed_string": "VBScriptUnclosedString",
        "xml_end": "XMLEnd",
        "xml_start": "XMLStart",
        "xml_tag_end": "XMLTagEnd"
    },
    "idl": {
        # this uses the "cpp" token set
    },
    "java": {
        # this uses the "cpp" token set
    },
    "javascript": {
        # this uses the "cpp" token set
    },
    "lua": {
        "basic_functions": "BasicFunctions",
        "character": "Character",
        "comment": "Comment",
        "coroutines_io_system_facilities": "CoroutinesIOSystemFacilities",
        "default": "Default",
        "identifier": "Identifier",
        "keyword": "Keyword",
        "keyword_set5": "KeywordSet5",
        "keyword_set6": "KeywordSet6",
        "keyword_set7": "KeywordSet7",
        "keyword_set8": "KeywordSet8",
        "label": "Label",
        "line_comment": "LineComment",
        "literal_string": "LiteralString",
        "number": "Number",
        "operator": "Operator",
        "preprocessor": "Preprocessor",
        "string": "String",
        "string_table_maths_functions": "StringTableMathsFunctions",
        "unclosed_string": "UnclosedString"
    },
    "makefile": {
        "comment": "Comment",
        "default": "Default",
        "error": "Error",
        "operator": "Operator",
        "preprocessor": "Preprocessor",
        "target": "Target",
        "variable": "Variable"
    },
    "matlab": {
        "command": "Command",
        "comment": "Comment",
        "default": "Default",
        "double_quoted_string": "DoubleQuotedString",
        "identifier": "Identifier",
        "keyword": "Keyword",
        "number": "Number",
        "operator": "Operator",
        "single_quoted_string": "SingleQuotedString"
    },
    "octave": {
        # this uses the "matlab" token set
    },
    "pascal": {
        "asm": "Asm",
        "character": "Character",
        "comment": "Comment",
        "comment_line": "CommentLine",
        "comment_parenthesis": "CommentParenthesis",
        "default": "Default",
        "hex_number": "HexNumber",
        "identifier": "Identifier",
        "keyword": "Keyword",
        "number": "Number",
        "operator": "Operator",
        "pre_processor": "PreProcessor",
        "pre_processor_parenthesis": "PreProcessorParenthesis",
        "single_quoted_string": "SingleQuotedString",
        "unclosed_string": "UnclosedString"
    },
    "perl": {
        "array": "Array",
        "backtick_here_document": "BacktickHereDocument",
        "backtick_here_document_var": "BacktickHereDocumentVar",
        "backticks": "Backticks",
        "backticks_var": "BackticksVar",
        "comment": "Comment",
        "data_section": "DataSection",
        "default": "Default",
        "double_quoted_here_document": "DoubleQuotedHereDocument",
        "double_quoted_here_document_var": "DoubleQuotedHereDocumentVar",
        "double_quoted_string": "DoubleQuotedString",
        "double_quoted_string_var": "DoubleQuotedStringVar",
        "error": "Error",
        "format_body": "FormatBody",
        "format_identifier": "FormatIdentifier",
        "hash": "Hash",
        "here_document_delimiter": "HereDocumentDelimiter",
        "identifier": "Identifier",
        "keyword": "Keyword",
        "number": "Number",
        "operator": "Operator",
        "pod": "POD",
        "pod_verbatim": "PODVerbatim",
        "quoted_string_q": "QuotedStringQ",
        "quoted_string_qq": "QuotedStringQQ",
        "quoted_string_qq_var": "QuotedStringQQVar",
        "quoted_string_qr": "QuotedStringQR",
        "quoted_string_qr_var": "QuotedStringQRVar",
        "quoted_string_qw": "QuotedStringQW",
        "quoted_string_qx": "QuotedStringQX",
        "quoted_string_qx_var": "QuotedStringQXVar",
        "regex": "Regex",
        "regex_var": "RegexVar",
        "scalar": "Scalar",
        "single_quoted_here_document": "SingleQuotedHereDocument",
        "single_quoted_string": "SingleQuotedString",
        "subroutine_prototype": "SubroutinePrototype",
        "substitution": "Substitution",
        "substitution_var": "SubstitutionVar",
        "symbol_table": "SymbolTable",
        "translation": "Translation"
    },
    "postscript": {
        "array_parenthesis": "ArrayParenthesis",
        "bad_string_character": "BadStringCharacter",
        "base85_string": "Base85String",
        "comment": "Comment",
        "default": "Default",
        "dictionary_parenthesis": "DictionaryParenthesis",
        "dsc_comment": "DSCComment",
        "dsc_comment_value": "DSCCommentValue",
        "hex_string": "HexString",
        "immediate_eval_literal": "ImmediateEvalLiteral",
        "keyword": "Keyword",
        "literal": "Literal",
        "name": "Name",
        "number": "Number",
        "procedure_parenthesis": "ProcedureParenthesis",
        "text": "Text"
    },
    "pov": {
        "bad_directive": "BadDirective",
        "comment": "Comment",
        "comment_line": "CommentLine",
        "default": "Default",
        "directive": "Directive",
        "identifier": "Identifier",
        "keyword_set6": "KeywordSet6",
        "keyword_set7": "KeywordSet7",
        "keyword_set8": "KeywordSet8",
        "number": "Number",
        "objects_csg_appearance": "ObjectsCSGAppearance",
        "operator": "Operator",
        "predefined_functions": "PredefinedFunctions",
        "predefined_identifiers": "PredefinedIdentifiers",
        "string": "String",
        "types_modifiers_items": "TypesModifiersItems",
        "unclosed_string": "UnclosedString"
    },
    "properties": {
        "assignment": "Assignment",
        "comment": "Comment",
        "default": "Default",
        "default_value": "DefaultValue",
        "key": "Key",
        "section": "Section"
    },
    "python": {
        "class_name": "ClassName",
        "comment": "Comment",
        "comment_block": "CommentBlock",
        "decorator": "Decorator",
        "default": "Default",
        "double_quoted_string": "DoubleQuotedString",
        "double_quoted_fstring": "DoubleQuotedFString",
        "function_method_name": "FunctionMethodName",
        "highlighted_identifier": "HighlightedIdentifier",
        "identifier": "Identifier",
        "keyword": "Keyword",
        "number": "Number",
        "operator": "Operator",
        "single_quoted_string": "SingleQuotedString",
        "single_quoted_fstring": "SingleQuotedFString",
        "triple_double_quoted_string": "TripleDoubleQuotedString",
        "triple_double_quoted_fstring": "TripleDoubleQuotedFString",
        "triple_single_quoted_string": "TripleSingleQuotedString",
        "triple_single_quoted_fstring": "TripleSingleQuotedFString",
        "unclosed_string": "UnclosedString"
    },
    "ruby": {
        "backticks": "Backticks",
        "class_name": "ClassName",
        "class_variable": "ClassVariable",
        "comment": "Comment",
        "data_section": "DataSection",
        "default": "Default",
        "demoted_keyword": "DemotedKeyword",
        "double_quoted_string": "DoubleQuotedString",
        "error": "Error",
        "function_method_name": "FunctionMethodName",
        "global": "Global",
        "here_document": "HereDocument",
        "here_document_delimiter": "HereDocumentDelimiter",
        "identifier": "Identifier",
        "instance_variable": "InstanceVariable",
        "keyword": "Keyword",
        "module_name": "ModuleName",
        "number": "Number",
        "operator": "Operator",
        "percent_string_q": "PercentStringQ",
        "percent_stringq": "PercentStringq",
        "percent_stringr": "PercentStringr",
        "percent_stringw": "PercentStringw",
        "percent_stringx": "PercentStringx",
        "pod": "POD",
        "regex": "Regex",
        "single_quoted_string": "SingleQuotedString",
        "stderr": "Stderr",
        "stdin": "Stdin",
        "stdout": "Stdout",
        "symbol": "Symbol"
    },
    "spice": {
        "command": "Command",
        "comment": "Comment",
        "default": "Default",
        "delimiter": "Delimiter",
        "function": "Function",
        "identifier": "Identifier",
        "number": "Number",
        "parameter": "Parameter",
        "value": "Value"
    },
    "sql": {
        "comment": "Comment",
        "comment_doc": "CommentDoc",
        "comment_doc_keyword": "CommentDocKeyword",
        "comment_doc_keyword_error": "CommentDocKeywordError",
        "comment_line": "CommentLine",
        "comment_line_hash": "CommentLineHash",
        "default": "Default",
        "double_quoted_string": "DoubleQuotedString",
        "identifier": "Identifier",
        "keyword": "Keyword",
        "keyword_set5": "KeywordSet5",
        "keyword_set6": "KeywordSet6",
        "keyword_set7": "KeywordSet7",
        "keyword_set8": "KeywordSet8",
        "number": "Number",
        "operator": "Operator",
        "plus_comment": "PlusComment",
        "plus_keyword": "PlusKeyword",
        "plus_prompt": "PlusPrompt",
        "quoted_identifier": "QuotedIdentifier",
        "single_quoted_string": "SingleQuotedString"
    },
    "tcl": {
        "comment": "Comment",
        "comment_block": "CommentBlock",
        "comment_box": "CommentBox",
        "comment_line": "CommentLine",
        "default": "Default",
        "expand_keyword": "ExpandKeyword",
        "identifier": "Identifier",
        "itcl_keyword": "ITCLKeyword",
        "keyword_set6": "KeywordSet6",
        "keyword_set7": "KeywordSet7",
        "keyword_set8": "KeywordSet8",
        "keyword_set9": "KeywordSet9",
        "modifier": "Modifier",
        "number": "Number",
        "operator": "Operator",
        "quoted_keyword": "QuotedKeyword",
        "quoted_string": "QuotedString",
        "substitution": "Substitution",
        "substitution_brace": "SubstitutionBrace",
        "tcl_keyword": "TCLKeyword",
        "tk_command": "TkCommand",
        "tk_keyword": "TkKeyword"
    },
    "tex": {
        "command": "Command",
        "default": "Default",
        "group": "Group",
        "special": "Special",
        "symbol": "Symbol",
        "text": "Text"
    },
    "verilog": {
        "comment": "Comment",
        "comment_bang": "CommentBang",
        "comment_line": "CommentLine",
        "default": "Default",
        "identifier": "Identifier",
        "keyword": "Keyword",
        "keyword_set2": "KeywordSet2",
        "number": "Number",
        "operator": "Operator",
        "preprocessor": "Preprocessor",
        "string": "String",
        "system_task": "SystemTask",
        "unclosed_string": "UnclosedString",
        "user_keyword_set": "UserKeywordSet"
    },
    "vhdl": {
        "attribute": "Attribute",
        "comment": "Comment",
        "comment_line": "CommentLine",
        "default": "Default",
        "identifier": "Identifier",
        "keyword": "Keyword",
        "keyword_set7": "KeywordSet7",
        "number": "Number",
        "operator": "Operator",
        "standard_function": "StandardFunction",
        "standard_operator": "StandardOperator",
        "standard_package": "StandardPackage",
        "standard_type": "StandardType",
        "string": "String",
        "unclosed_string": "UnclosedString"
    },
    "xml": {
        # this uses the "html" token set
    },
    "yaml": {
        "comment": "Comment",
        "default": "Default",
        "document_delimiter": "DocumentDelimiter",
        "identifier": "Identifier",
        "keyword": "Keyword",
        "number": "Number",
        "operator": "Operator",
        "reference": "Reference",
        "syntax_error_marker": "SyntaxErrorMarker",
        "text_block_marker": "TextBlockMarker"
    }
}


TOKENS["csharp"] = TOKENS["cpp"]
TOKENS["enaml"] = TOKENS["python"]
TOKENS["fortran"] = TOKENS["fortran77"]
TOKENS["idl"] = TOKENS["cpp"]
TOKENS["java"] = TOKENS["cpp"]
TOKENS["javascript"] = TOKENS["cpp"]
TOKENS["octave"] = TOKENS["matlab"]
TOKENS["xml"] = TOKENS["html"]
