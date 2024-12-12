<div align="center">
	<img src="./logo.svg" alt="Black and White logo" width="100">
	<h1>Black and White</h1>
	<h3>The not that munch compromising Python code formatter</h3>
</div>

Black and White aims to provide a highly customizable Python code formatting
experience, offering an alternative to Black while maintaining a similar level
of automation and ease of use.  It strives for a balance between enforcing
consistent code style and allowing developers to tailor the formatting to their preferences.

## Key Features

* **Customizability:**  Configure various formatting aspects to match your coding
  style or team conventions.
* **Extensibility:** Easily add support for new language features or custom
  formatting rules.
* **Performance:**  Efficiently formats even large codebases.

## Installation

```shell
pip install black-and-white
```

## Usage

```txt
usage:
          black-and-white [-h] [--version] [--config <config_path>] <path>
python -m black_and_white [-h] [--version] [--config <config_path>] <path>

The not that munch compromising Python code formatter

positional arguments:
  <path>                Path to the file or directory to format

options:
  -h, --help            show this help message and exit
  --version, -V         show program's version number and exit
  --config, -c <config_path>
                        Path to configuration file. Default to ./.black-and-
                        white.toml. Use - for stdin
```

## Configuration

Configuration options are specified via a configuration file (`.black-and-white.toml`).
See [`docs/configuration.md`](./docs/configuration.md) for details on available options.

## License

Black and White is licensed under the [GNU General Public License v2.0-only](https://www.gnu.org/licenses/gpl-2.0),
see [`LICENSE`](./LICENSE) for more information.
