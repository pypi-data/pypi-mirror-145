from distutils.core import setup

VERSION = '1.0.5'
PACKAGE_NAME = 'terraria-xbox360-player-api'
AUTHOR = 'Filip K'
AUTHOR_EMAIL = 'fkwilczek@gmail.com'
URL = 'https://gitlab.com/fkwilczek/terraria-xbox360-player-api'

LICENSE = 'GNU General Public License v3 (GPLv3)'
DESCRIPTION = 'API for reading and modifying xbox 360 terraria player files.'
LONG_DESCRIPTION = open('README.md', encoding='utf-8').read()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
	'bitarray',
	'binary-rw',
	'terraria-apis-objects'
]

setup(
	name=PACKAGE_NAME,
	version=VERSION,
	author=AUTHOR,
	author_email=AUTHOR_EMAIL,
	description=DESCRIPTION,
	long_description=LONG_DESCRIPTION,
	long_description_content_type=LONG_DESC_TYPE,
	url=URL,
	license=LICENSE,
	install_requires=INSTALL_REQUIRES,
	classifiers=[
		'Programming Language :: Python :: 3',
		'Operating System :: OS Independent',
		'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
	],
	packages=['terraria_xbox360_player_api'],
)
