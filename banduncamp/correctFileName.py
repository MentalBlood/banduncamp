import re



def correctFileName(name: str):
	return re.sub(
		r'[\/\\:\*\?"\<\>|]',
		'',
		name.strip('. ')
	)