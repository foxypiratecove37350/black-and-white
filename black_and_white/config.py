"""Black and White: The not that munch compromising Python code formatter

Author: foxy pirate cove / Fnaf
License: GNU General Public License v2.0 only (GPL-2.0)
Version: 0.1.0

Configuration management
"""

from enum import Enum
from dataclasses import dataclass
from pathlib import Path
from sys import stdin
from tomllib import load


class IndentType(Enum):
	"""Types of indentation to use"""

	TABS: str = 'tabs'
	SPACES: str = 'spaces'


class QuoteType(Enum):
	"""Types of quotes to use"""

	SINGLE: str = 'single'
	DOUBLE: str = 'double'


class EndOfLine(Enum):
	"""Types of end of lines to use"""

	LF: str = 'lf'
	CRLF: str = 'crlf'
	CR: str = 'cr'


@dataclass
class Config:
	"""Class to hold the configuration"""

	line_length: int = 88
	prose_wrap: bool = False
	indent_type: IndentType = IndentType.SPACES
	indent_width: int = 4
	quote_type: QuoteType = QuoteType.SINGLE
	trailing_comma: bool = True
	bracket_spacing: bool = False
	end_of_line: EndOfLine = EndOfLine.LF

	def __post_init__(self):
		"""Validate the configuration
		
		Raises:
			TypeError, ValueError: If the configuration is invalid

		"""

		if not isinstance(self.line_length, int):
			raise TypeError('line_length must be an integer')
		
		if not isinstance(self.prose_wrap, bool):
			raise TypeError('prose_wrap must be a boolean')
		
		if self.indent_type not in IndentType:
			raise ValueError(f'indent_type must be in {[e.value for e in IndentType]}')
		
		if not isinstance(self.indent_width, int):
			raise TypeError('indent_width must be an integer')
		
		if self.quote_type not in QuoteType:
			raise ValueError(f'quote_type must be a in {[e.value for e in QuoteType]}')
		
		if not isinstance(self.trailing_comma, bool):
			raise TypeError('trailing_comma must be a boolean')
		
		if not isinstance(self.bracket_spacing, bool):
			raise TypeError('bracket_spacing must be a boolean')
		
		if self.end_of_line not in EndOfLine:
			raise ValueError(f'end_of_line must be in {[e.value for e in EndOfLine]}')
		
		self.indent_type = IndentType(self.indent_type)
		self.quote_type = QuoteType(self.quote_type)
		self.end_of_line = EndOfLine(self.end_of_line)


def parse_config(config_file_path: Path) -> Config:
	"""Parses the TOML configuration file and returns a Config object

	Args:
		config_file_path (Path): Path to the configuration file

	Returns:
		Config: Config object

	Raises:
		TypeError, ValueError: If the configuration is invalid
	
	"""

	config_dict: dict = {}
	config: dict = {}

	if config_file_path == Path('-'):
		config_dict = load(stdin.buffer)
	elif not config_file_path.is_file():
		if (config_file_path.parent / '.black-and-white.toml').is_file():
			config_file_path = (config_file_path.parent / '.black-and-white.toml')
		elif (config_file_path.parent / 'pyproject.toml').is_file():
			config_file_path = (config_file_path.parent / 'pyproject.toml')

	try:
		config_dict = load(config_file_path.open('rb'))
		try:
			if 'black-and-white' in config_dict.keys():
				config = config_dict['black-and-white']
			else:
				config = config_dict['tool']['black-and-white']
		except KeyError:
			raise ValueError(f'\'{config_file_path}\' is not a Black and White configuration file')
	except FileNotFoundError:
		pass

	return Config(**config)
