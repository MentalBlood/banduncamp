from setuptools import setup, find_packages


if __name__ == '__main__':

	setup(

		name             = 'banduncamp',
		version          = '2.0.0',
		python_requires  = '>=3.11',
		install_requires = [
			'bs4',
			'yoop',
			'pytags'
		],
		keywords = ['downloader'],
		url      = 'https://github.com/MentalBlood/banduncamp',

		description                   = 'Tool for downloading music from bandcamp',
		long_description              = open('README.md').read(),
		long_description_content_type = 'text/markdown',

		classifiers = [
			'Development Status :: 5 - Production/Stable',
			'Intended Audience :: End Users/Desktop'
			'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
			'Typing :: Typed',
			'Operating System :: OS Independent',
			'Programming Language :: Python :: 3.10',
			'License :: OSI Approved :: BSD License'
		],

		author           = 'mentalblood',
		author_email     = 'neceporenkostepan@gmail.com',
		maintainer       = 'mentalblood',
		maintainer_email = 'neceporenkostepan@gmail.com',

		packages = find_packages()

	)
