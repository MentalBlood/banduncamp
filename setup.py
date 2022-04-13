import os
from setuptools import setup, find_packages


if __name__ == '__main__':

	long_description = ''
	if os.path.exists('README.md'):
		with open('README.md', encoding='utf-8') as f:
			long_description = f.read()

	setup(
		name='banduncamp',
		version='1.0.0',
		description='Fast tool for downloading audio from bandcamp',
		long_description=long_description,
		long_description_content_type='text/markdown',
		author='mentalblood',
		install_requires=[
			'bs4',
			'requests',
			'tqdm',
			'mutagen',
			'python_version >= "3.10"'
		],
		packages=find_packages()
	)
