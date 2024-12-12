# Configuration - Black and White Documenation

Black and White Configuration

Black and White uses a TOML file for configuration. You can specify the path to this file using the
`--config` flag. If no config file is specified, Black and White defaults to searching for
`.black-and-white.toml` in the current directory. Alternatively, configurations can also be nested
under the `tool.black-and-white` table in a `pyproject.toml` file.

Formatting Options:

* `line_length` (integer, default: 88): Sets the maximum line length. Lines longer than this value
  will be wrapped.
* `prose_wrap` (boolean, default: `false`): Controls whether long lines in comments and docstrings
  are wrapped.
* `indent_type` (string, default: "spaces"): Specifies the type of indentation to use. Valid values
  are `"tabs"` and `"spaces"`.
* `indent_width` (integer, default: 4): Sets the number of spaces or tabs to use for indentation
  (depending on `indent_type`).
* `quote_type` (string, default: "single"): Specifies the type of quotes to use for strings. Valid
  values are `"single"` and `"double"`.
* `trailing_comma` (boolean, default: `true`): Controls whether to add a trailing comma after the
  last element in lists, tuples, and dictionaries.
* `bracket_spacing` (boolean, default: `false`): If `true`, inserts spaces between curly braces `{}`
  and the values they contain. For example: `{ key: value }` vs. `{key: value}`.  This option does
  *not* affect spacing within square brackets `[]` or parentheses `()`.
* `end_of_line` (string, default: "lf"): Specifies the type of line ending to use. Valid values are
  `"lf"`, `"crlf"`, and `"cr"`.

Example Configuration (`.black-and-white.toml`):

```toml
[black-and-white]
line_length = 100
prose_wrap = true
indent_type = "tabs"
quote_type = "double"
trailing_comma = false
bracket_spacing = true
end_of_line = "crlf"
```

Example Configuration within `pyproject.toml`:

```toml
# ...

[tool.black-and-white]
line_length = 100
prose_wrap = true
indent_type = "tabs"
quote_type = "double"
trailing_comma = false
bracket_spacing = true
end_of_line = "crlf"

# ...
```

If an option is not specified in the configuration file, the default value will be used.
