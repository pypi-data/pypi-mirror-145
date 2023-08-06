# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fdpm']

package_data = \
{'': ['*']}

install_requires = \
['python-Levenshtein>=0.12.2,<0.13.0',
 'pythondialog>=3.5.3,<4.0.0',
 'requests>=2.27.1,<3.0.0',
 'thefuzz>=0.19.0,<0.20.0',
 'tqdm>=4.63.0,<5.0.0']

entry_points = \
{'console_scripts': ['fdpm = fdpm.__main__:main']}

setup_kwargs = {
    'name': 'fdpm',
    'version': '0.0.74',
    'description': 'Command line tool to install packages from f-droid.org',
    'long_description': '# fdpm\n\nF-Droid Package Manager\nInstall apps from f-droid through command line\n\n## Requirements\n- adb\n- python\n\n## Setup\n- On android:\n  - [Enable adb from developer options](https://developer.android.com/studio/command-line/adb#Enabling)\n  - [Optional but recommended] To connect adb on phone itself\n      - Install [termux](https://f-droid.org/en/packages/com.termux/) \n      - Install [adb binaries](https://github.com/ShiSheng233/Termux-ADB)\n      - Follow steps for Wireless connection [here](https://github.com/mzlogin/awesome-adb/blob/master/README.en.md#wireless-connection-need-to-use-the-usb-cable) (Needs USB one time)\n      - After disconnecting usb, use termux to connect adb.\n- On desktop:\n  - Download and extract [platform tools](https://developer.android.com/studio/releases/platform-tools#downloads)\n  - Add `adb` to your `PATH` (You should be able to access it from any directory)\n  - Follow connection steps for [wireless](https://github.com/mzlogin/awesome-adb/blob/master/README.en.md#wireless-connection-need-to-use-the-usb-cable) \n  or [usb](https://github.com/mzlogin/awesome-adb/blob/master/README.en.md#wireless-connection-need-to-use-the-usb-cable)\n- Install [dummy installer apk](https://gitlab.com/kshib/fdpm/-/blob/main/fdroid-cli.apk)\n  ([Source code](https://gitlab.com/kshib/fdpm-installer)) - Needed to track installed apps by fdpm\n\n## Installation\n```\npip install fdpm\n```\n\n## Usage\n````\n# Search apps\nfdpm -s launcher\n\n# Install apps\nfdpm -i org.videolan.vlc ch.deletescape.lawnchair.plah\n\n# Uninstall apps\nfdpm -n org.videolan.vlc ch.deletescape.lawnchair.plah\n\n# Update installed apps\nfdpm -u\n\n# Use dialog interface to avoid using package names (Not supported on windows)\nfdpm -d\n\n# Repo names:\nfdpm -a\n\n# Subscribe to repo\nfdpm -a Bitwarden\n\n# Unsubscribe from repo\nfdpm -r Bitwarden\n\n````\n\nScreenshots:\n![dialog_demo](https://z.zz.fo/9DeTS.jpg "Dialog demo")\n\n## Tested on\n- Android 11\n- 5.16.14-1-MANJARO\n\n## License\nGNU AFFERO GENERAL PUBLIC LICENSE\n\n',
    'author': 'Kshitij Bhuwad',
    'author_email': 'ksyko@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/kshib/fdpm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.0,<4.0.0',
}


setup(**setup_kwargs)
