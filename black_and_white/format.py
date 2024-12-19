"""Black and White: The not that much compromising Python code formatter

Author: foxy pirate cove / Fnaf
License: GNU General Public License v2.0 only (GPL-2.0)
Version: 0.1.0

Formatting
"""

from asyncio import (
	run as async_run,
	gather as async_run_all
)
from collections.abc import Generator
from itertools import chain
from pathlib import Path

from .config import Config
from .parsing import Token, parse


async def async_rglob(path: Path, pattern: str) -> Generator[Path, None, None]:
	return path.rglob(pattern)


def format_code(path: Path, config: Config) -> None:
	"""Formats the given path according to the given config

	Args:
		path (Path): Path to the file or directory to format
		config (Config): Config object

	Raises:
		FileNotFoundError: When ``path`` isn't found

	"""

	if path.is_dir():
		async_run(format_dir(path, config))
	else:
		async_run(format_file(path, config))


async def format_dir(dir_path: Path, config: Config) -> None:
	"""Formats the given directory according to the given config

	Args:
		dir_path (Path): Path to the directory to format
		config (Config): Config object

	Raises:
		FileNotFoundError: When ``dir_path`` isn't found
	
	"""

	matched_files: tuple = await async_run_all(
		async_rglob(dir_path, '*.py'),
		async_rglob(dir_path, '*.pyi'),
		async_rglob(dir_path, '*.pyt')
	)

	await async_run_all(*map(
		lambda file_path: format_file(file_path, config),
		chain(*matched_files)
	))


async def format_file(file_path: Path, config: Config) -> None:
	"""Formats the given file according to the given config

	Args:
		file_path (Path): Path to the file to format
		config (Config): Config object

	Raises:
		FileNotFoundError: When ``file_path`` isn't found
	
	"""

	content: str = open(file_path, 'r', encoding='utf-8').read()

	try:
		parsed_content = parse(content)
	except Exception as e:
		raise e.__class__(f'File \'{file_path}\': {e}')

	print(f'Formatted \'{file_path}\'')
