# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arkive',
 'arkive.actions',
 'arkive.console',
 'arkive.core',
 'arkive.drives',
 'arkive.drives.local',
 'arkive.drives.pcloud',
 'arkive.utility']

package_data = \
{'': ['*']}

install_requires = \
['beautifultable>=1.0.1,<2.0.0',
 'pathvalidate>=2.5.0,<3.0.0',
 'tinytag>=1.8.1,<2.0.0',
 'wcwidth>=0.2.5,<0.3.0']

entry_points = \
{'console_scripts': ['arkive = arkive.__main__:main']}

setup_kwargs = {
    'name': 'arkive',
    'version': '0.3.1',
    'description': 'Manage your music/audio collections.',
    'long_description': '# Arkive\n\nManage your music/audio collections.\n\n## 1. Installation\n\nA package with the same name is available in [pypi](https://pypi.org/project/arkive)\n\n```\n  $ pip install --user arkive\n```\n\nThis package has been tested mainly on Windows 10 and Linux (Fedora 35), but it should work on all platforms since it\nonly makes use of cross-platform libraries. You may need to use "pip3", "python3 -m pip" or "python -m" when running on\nother platforms, or different Python setups.\n\nYou can also use pipx to only make use of the cli app.\n\n```\n  $ pipx install arkive\n```\n\n## 2. General usage\n\n```\n$ arkive -h\nusage: arkive [-h] [-V] <command> ...\n\noptional arguments:\n  -h, --help     show this help message and exit\n  -V, --version  show program\'s version number and exit\n\ncommands:\n  <command>\n    show         display actions collection inside a given folder.\n    flat         flatten actions files inside a given folder.\n    nest         nesting actions files inside a given folder.\n```\n\nAs explained above, you can use one of 3 commands: show, flat and nest, and finally a positional argument indicating a\nfolder path.\n\n### show\n\nIt will traverse the folders inside the given path and display a table of all the existing (with compatible audio\nformats) files, showing artist, album and title.\n\n```\n$ arkive show ~/Music\n```\n\n### flat\n\nThe application will traverse all the subfolders and move the music files up to the given folder while changing their\nname. The new name given to each file will be a concatenation of its artist, album and title.\n\n*e.g.* .../folder/subfolder/myfile.mp3 -> .../folder/artist - album - title.mp3\n\n**Note:** the new name will be sanitized to make sure the result is a valid filename.\n\n```\n$ arkive flat ~/Music\n```\n\n### nest\n\nThe application will traverse all the subfolders and move the music files up to the given folder while renaming name\norganizing them in new subfolders. The names given to each file and folder structures will result from taking the artist\nand album names for the folders, and track title for its name.\n\n*e.g.* .../folder/subfolder/myfile.mp3 -> .../folder/artist/album/title.mp3\n\n**Note:** the new names for each file and folder will be sanitized to make sure the result is a valid file/directory.\n\n```\n$ arkive nest ~/Music\n```\n\n#### Destination folder\n\nAn optional argument "-o/-output" may be used to change the destination directory for the audio files.\n\n## 3. Web storage support (Experimental)\n\nAdditionally, arkive includes support for web storage with the same commands shown above. As of now, only pcloud service\nis supported but other may be included in the future. To use a command with your pcloud account, pass the "--cloud" flag\nfollowed by the name if the services (e.g. pcloud), and then your user credentials.\n\n```\n$ arkive show "/My Music" --cloud pcloud --username <USERNAME> --password <PASSWORD>\n```\n\n## 4. Side-effects\n\nThis implementation includes a "cleanup" procedure which removes empty sub-folders from the origin directory. This is a\npersonal decision due to its convenience, but it may be changed in the near future to remove them only under explicit\nindication.',
    'author': 'Orlando Ospino Sánchez',
    'author_email': 'oroschz@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/oroschz/arkive',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
