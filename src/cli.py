from argparse import ArgumentParser, Namespace
from pathlib import Path

def main() -> None:
	arg_parser: ArgumentParser = ArgumentParser(
		'black-and-white',
		description='The not that munch compromising Python code formatter'
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
