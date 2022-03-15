import re



special_characters = re.compile(r'[\/\\:\*\?"\<\>|]')


def correctFileName(name: str):
	return re.sub(
		special_characters,
		'',
		name
	)