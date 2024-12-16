"""Black and White: The not that munch compromising Python code formatter

Author: foxy pirate cove / Fnaf
License: GNU General Public License v2.0 only (GPL-2.0)
Version: 0.1.0

Parsing
"""

import keyword
import string

from dataclasses import dataclass
from enum import Enum, auto
from typing import Generic, TypeVar


class TokenType(Enum):
	KEYWORD: str = 'keyword'
	IDENTIFIER: str = 'identifier'
	OPERATOR: str = 'operator'
	COMMENT: str = 'comment'
	STRING: str = 'string'
	NUMBER: str = 'number'
	PUNCTUATION: str = 'punctuation'
	INDENT: str = 'indent'
	NEWLINE: str = 'newline'
	EOF: str = 'eof'


T = TypeVar('T')
@dataclass
class Token(Generic[T]):
	type: TokenType
	content: T

	def __post_init__(self):
		if self.type not in TokenType:
			raise ValueError(f'type must be in {[e.value for e in TokenType]}')

def lexing(content: str) -> list[Token]:
	tokens: list[Token] = []
	i: int = 0

	try:
		while i < len(content):
			c: str = content[i]

			if c in '\t ' and content[i - 1] in '\r\n':
				... # Have to find the indent size to continue
			elif c in '\t ':
				i += 1
			elif c in '\r\n;':
				tokens.append(Token(
					TokenType.NEWLINE,
					c + (content[i + 1] if c == '\r' and content[i + 1] == '\n' else '')
				))

				i += 1
			elif c == '#':
				comment: str = ''
				i += 1

				if content[i] == ' ':
					i += 1

				while content[i] not in '\r\n':
					comment += content[i]
					i += 1

				tokens.append(Token(TokenType.COMMENT, comment))
			elif c.lower() in 'bfru' and (
				(content[i + 1].lower() in 'bfru'.replace(c, '') and content[i + 2] in '\'"')
				or content[i + 1] in '\'"'
			):
				i += 1 if content[i + 1] in '\'"' else 2
			elif c in '\'"':
				quote: str = c
				string_content: str = ''
				prefixes: str = ''

				if content[i - 1].lower() in 'bfru':
					prefixes = content[i - 1]
					prefixes += content[i - 2] if content[i - 2].lower() in 'bfru'.replace(prefixes, '') else ''

					prefixes = ''.join(sorted(prefixes))

					if len(prefixes) != 1 and 'u' in prefixes:
						raise SyntaxError('Can\'t combine \'u\' prefix with other prefixes')
					
					if prefixes == 'bf':
						raise SyntaxError('Can\'t combine \'f\' and \'b\' prefixes')
					
				if content[i + 1] + content[i + 2] == quote * 2:
					quote += quote * 2
					i += 2

				i += 1
				backslashes_count: int = 0

				while not (content[i : i + len(quote)] == quote and backslashes_count % 2 == 0):
					if content[i] in '\r\n' and len(quote) != 3 and backslashes_count % 2 == 0:
						raise SyntaxError('Unterminated string literal')
					elif content[i] in '\r\n' and len(quote) != 3 and backslashes_count % 2 == 1:
						string_content = string_content[:-1]
						i += 1
						backslashes_count = 0
						continue

					if content[i] == '\\':
						backslashes_count += 1
					else:
						backslashes_count = 0

					string_content += content[i]
					i += 1

				i += len(quote)
					
				tokens.append(Token(TokenType.STRING, (prefixes, string_content)))
			elif c in '0123456789':
				dot_count: int = 0
				number: str = c
				i += 1

				while content[i] in '0123456789.':
					if content[i] == '.':
						dot_count += 1

						if dot_count > 1:
							raise SyntaxError('Too many decimal points in number')

					number += content[i]
					i += 1

				tokens.append(Token(TokenType.NUMBER, float(number) if '.' in number else int(number)))
			elif c in string.ascii_letters + '_':
				identifier: str = c
				i += 1

				while content[i] in string.ascii_letters + string.digits + '_':
					identifier += content[i]
					i += 1

				if content[i] in '\'"':
					raise SyntaxError('Invalid syntax')

				tokens.append(Token(
					TokenType.KEYWORD if keyword.iskeyword(identifier) else TokenType.IDENTIFIER,
					identifier
				))
			elif c in '+-*/%@=!><&|^~':
				operator: str = c
				i += 1

				if c in '*/=<>' and content[i] == c:
					operator += content[i]
					i += 1

				if operator in (
					'+',
					'-',
					'*',
					'/',
					'%',
					'//',
					'**',
					'@',
					'&',
					'|',
					'^',
					'>>',
					'<<',
					'!',
					'>',
					'<'
				) and content[i] == '=':
					operator += content[i]
					i += 1

				if operator == '!':
					raise SyntaxError(f'Invalid operator {operator!r}')

				tokens.append(Token(TokenType.OPERATOR, operator))
			elif c in ':.,()[]{}\\':
				i += 1

				if c == ':' and content[i] == '=':
					tokens.append(Token(TokenType.OPERATOR, ':='))
					continue

				if c == '.' and content[i] in string.digits and tokens[-1].type not in (
					TokenType.IDENTIFIER,
					TokenType.STRING,
					TokenType.NUMBER
				):
					number = '0.'

					while content[i] in '0123456789.':
						if content[i] == '.':
							raise SyntaxError('Too many decimal points in number')

						number += content[i]
						i += 1

					tokens.append(Token(TokenType.NUMBER, float(number)))
					continue
				elif c == '.' and content[i] in string.digits:
					raise SyntaxError('Invalid syntax') # Need to find a better error message

				tokens.append(Token(TokenType.PUNCTUATION, c))
			else:
				print(f'Unexpected character {c!r}')
				i += 1
	except Exception as e:
		content_before: str = content[: i + 1]
		ln: int = content_before.count('\n') + 1
		col: int = len(content_before) - content_before.rfind('\n') - 1

		raise e.__class__(f'Line {ln}:{col}: {e}')

	tokens.append(Token(TokenType.EOF, i))

	return tokens


def parse(content: str):
	tokens: list[Token] = lexing(content)

