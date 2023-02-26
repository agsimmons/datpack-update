[![PyPI](https://img.shields.io/pypi/v/datpack-update)](https://pypi.org/project/datpack-update/)

# datpack-update
Update No-Intro DAT files

## Description
This script updates your current No-Intro dat files with new versions that you download. The benefit over doing this manually is that this program automatically finds which dat files you have in your existing folder, and only updates those dat files. This is helpful if you download the Daily datfile pack from [DAT-o-MATIC](https://datomatic.no-intro.org/).

Your dat files **must** be named exactly as DAT-o-MATIC names them. This program relies on the specific timestamp format being used. Some examples names are:

```
Atari - 2600 (20200514-091155).dat
Bandai - WonderSwan (20210609-224257).dat
Sega - Master System - Mark III (20210527-151920).dat
```

## Usage
```
usage: datpack-update [-h] src dest

Update No-Intro DAT files

positional arguments:
  src         Source directory of new DAT files
  dest        Destination directory of updated DAT files

optional arguments:
  -h, --help  show this help message and exit
```

## License
Copyright (C) 2023 Andrew Simmons

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
