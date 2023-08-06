# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ntfsdump', 'ntfsdump.models', 'ntfsdump.presenters', 'ntfsdump.views']

package_data = \
{'': ['*']}

install_requires = \
['libewf-python>=20201230,<20201231',
 'libvhdi-python>=20210425,<20210426',
 'libvmdk-python>=20210807,<20210808',
 'pytsk3>=20211111,<20211112']

entry_points = \
{'console_scripts': ['ntfsdump = ntfsdump.views.NtfsDumpView:entry_point']}

setup_kwargs = {
    'name': 'ntfsdump',
    'version': '2.4.0',
    'description': 'A tool for extract any files from an NTFS volume on an image file.',
    'long_description': "# ntfsdump\n\n[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)\n[![PyPI version](https://badge.fury.io/py/ntfsdump.svg)](https://badge.fury.io/py/ntfsdump)\n[![Python Versions](https://img.shields.io/pypi/pyversions/ntfsdump.svg)](https://pypi.org/project/ntfsdump/)\n[![pytest](https://github.com/sumeshi/ntfsdump/actions/workflows/test.yaml/badge.svg)](https://github.com/sumeshi/ntfsdump/actions/workflows/test.yaml)\n[![docker build](https://github.com/sumeshi/ntfsdump/actions/workflows/build-docker-image.yaml/badge.svg)](https://github.com/sumeshi/ntfsdump/actions/workflows/build-docker-image.yaml)\n\n![ntfsdump logo](https://gist.githubusercontent.com/sumeshi/c2f430d352ae763273faadf9616a29e5/raw/baa85b045e0043914218cf9c0e1d1722e1e7524b/ntfsdump.svg)\n\nA tool for extract any files from an NTFS volume on an image file.\n\n\n## Usage\n\n```bash\n$ ntfsdump {{query}} --output-path {{output_dir}} /path/to/imagefile.raw\n```\n\n```python\nfrom ntfsdump import ntfsdump\n\n# imagefile_path: str\n# output_path: str\n# target_queries: List[str]\n# volume_num: Optional[int] = None\n# file_type: Literal['raw', 'e01'] = 'raw'\n\nntfsdump(\n    imagefile_path='./path/to/your/imagefile.raw',\n    output_path='./path/to/output/directory',\n    target_queries=['/Windows/System32/winevt/Logs'],\n    volume_num=2,\n    file_type='raw'\n)\n```\n\n### Query\n\nBasically, enter the windows path to the file you want to extract.\nThe paths are separated by slashes.\n\ne.g.\n```\nOriginal Path: C:\\$MFT\nQuery: /$MFT\n\nOriginal Path: C:\\$Extend\\$UsnJrnl\\$J\nQuery: /$Extend/$UsnJrnl/$J\n\nOriginal Path: C:\\Windows\\System32\\winevt\\Logs\nQuery: /Windows/System32/winevt/Logs\n```\n\nQueries will be expanded in the future.\nIf you have any questions, please submit an issue.  \n\n\n### Example\nThe target path can be either alone or in a directory.\nIn the case of a directory, it dumps the lower files recursively.\n\n```.bash\n$ ntfsdump /Windows/System32/winevt/Logs -o ./dump ./path/to/your/imagefile.raw\n```\n\nextracting from E01 image (included splited-E01).\n\n```.bash\n$ ls\nimagefile.E01\nimagefile.E02\nimagefile.E03\nimagefile.E04\nimagefile.E05\n\n$ ntfsdump /Windows/System32/winevt/Logs --type=e01 -o ./dump ./path/to/your/imagefile.E01\n```\n\n#### When use with [ntfsfind](https://github.com/sumeshi/ntfsfind)\n\nhttps://github.com/sumeshi/ntfsfind\n\n```.bash\n$ ntfsfind '.*\\.evtx' ./path/to/your/imagefile.raw | ntfsdump ./path/to/your/imagefile.raw\n```\n\n### Options\n```\n--help, -h:\n    show help message and exit.\n\n--version, -v:\n    show program's version number and exit.\n\n--quiet, -q:\n    flat to suppress standard output.\n\n--nolog:\n    flag to no logs are output.\n\n--volume-num, -n:\n    NTFS volume number (default: autodetect).\n\n--type, -t:\n    Image file format (default: raw(dd-format)).\n    (raw|e01|vhd|vhdx|vmdk) are supported.\n\n--output-path, -o:\n    Output directory or file path.\n\n    If the target Path is a directory, the directory specified by --output-path is created and the target files is dump under it.\n\n    Otherwise, the file is dumped with the file name specified in the --output-path.)\n```\n\n## Prerequisites\nThe image file to be processed must meet the following conditions.\n\n- raw or e01 file format\n- NT file system(NTFS)\n- GUID partition table(GPT)\n\nAdditional file formats will be added in the future.  \nIf you have any questions, please submit an issue.  \n\n\n## LogFormat\nntfsdump outputs logs in the following format.  \nBy default, it outputs the files to the current directory, but if you do not need them, please use the `--nolog` option.\n\n```\n- ntfsdump v{{version}} - \n2022-01-01T00:00:00.000000: [{{EventName}}] {{Description}}\n2022-01-01T00:00:00.000000: [{{EventName}}] {{Description}}\n2022-01-01T00:00:00.000000: [{{EventName}}] {{Description}}\n...\n```\n\n\n## Installation\n\n### via PyPI\n\n```\n$ pip install ntfsdump\n```\n\n## Run with Docker\nhttps://hub.docker.com/r/sumeshi/ntfsdump\n\n\n```bash\n$ docker run --rm -v $(pwd):/app -t sumeshi/ntfsdump:latest '/$MFT' /app/sample.raw\n```\n\n## Contributing\n\nThe source code for ntfsdump is hosted at GitHub, and you may download, fork, and review it from this repository(https://github.com/sumeshi/ntfsdump).\n\nPlease report issues and feature requests. :sushi: :sushi: :sushi:\n\n## License\n\nntfsdump is released under the [LGPLv3+](https://github.com/sumeshi/ntfsdump/blob/master/LICENSE) License.\n\nPowered by [pytsk3](https://github.com/py4n6/pytsk), [libewf](https://github.com/libyal/libewf) and [ntfs-samples](https://github.com/msuhanov/ntfs-samples).\n",
    'author': 'sumeshi',
    'author_email': 'sum3sh1@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sumeshi/ntfsdump',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
