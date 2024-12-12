"""Black and White: The not that munch compromising Python code formatter

Author: foxy pirate cove / Fnaf
License: GNU General Public License v2.0 only (GPL-2.0)
Version: 0.1.0

CLI entrypoint
"""

from argparse import ArgumentParser, Namespace
from pathlib import Path

from .config import Config, parse_config
from . import __version__


def main() -> None:
	"""CLI entrypoint

	CLI Arguments:
		path (Path): Path to the file or directory to format
		config (Path, optional): Path to configuration file. Defaults to Path('./.black-and-white.toml'). Use - for stdin
	"""

	arg_parser: ArgumentParser = ArgumentParser(
		'black-and-white',
		description='The not that munch compromising Python code formatter'
	)
	arg_parser.add_argument(
		'--version',
		'-V',
		action='version',
		version=f'Black and White v{__version__}'
	)
	arg_parser.add_argument(
		'path',
		metavar='<path>',
		type=Path,
		help='Path to the file or directory to format'
	)
	arg_parser.add_argument(
		'--config',
		'-c',
		metavar='<config_path>',
		type=Path,
		default=Path('./.black-and-white.toml'),
		help='Path to configuration file. Default to ./.black-and-white.toml. Use - for stdin'
	)
	args: Namespace = arg_parser.parse_args()
	config: Config = parse_config(args.config)
