# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['s3fetch']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.15.18,<2.0.0', 'click>=8.0.0,<9.0.0', 'urllib3==1.26.8']

entry_points = \
{'console_scripts': ['s3fetch = s3fetch:cmd']}

setup_kwargs = {
    'name': 's3fetch',
    'version': '1.1.2',
    'description': 'Simple & fast multi-threaded S3 download tool.',
    'long_description': '# S3Fetch\n\nSimple & fast multi-threaded S3 download tool.\n\nSource: [https://github.com/rxvt/s3fetch](https://github.com/rxvt/s3fetch)\n\n![Build and Publish](https://github.com/rxvt/s3fetch/workflows/Build%20and%20Publish/badge.svg?branch=main)\n![Test](https://github.com/rxvt/s3fetch/workflows/Test/badge.svg?branch=development)\n[![PyPI version](https://badge.fury.io/py/s3fetch.svg)](https://badge.fury.io/py/s3fetch)\n\n## Features\n\n- Fast.\n- Simple to use.\n- Multi-threaded, allowing you to download multiple objects concurrently.\n- Quickly download a subset of objects under a prefix without listing all objects first.\n- Object listing occurs in a seperate thread and downloads start as soon as the first object key is returned while the object listing completes in the background.\n- Filter list of objects using regular expressions.\n- Uses standard Boto3 AWS SDK and standard AWS credential locations.\n- List only mode if you just want to see what would be downloaded.\n\n## Why use S3Fetch?\n\nTools such as the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html) and [s4cmd](https://pypi.org/project/s4cmd/) are great and offer a lot of features, but S3Fetch out performs them when downloading a subset of objects from a large S3 bucket.\n\nBenchmarking shows (see below) that S3Fetch can finish downloading 428 objects from a bucket containing 12,204,097 objects in 8 seconds while other tools have not started downloading a single object after 60 minutes.\n\n## Benchmarks\n\nDownloading 428 objects under the `fake-prod-data/2020-10-17` prefix from a bucket containing a total of 12,204,097 objects.\n\n#### With 100 threads\n\n```text\ns3fetch s3://fake-test-bucket/fake-prod-data/2020-10-17  --threads 100\n\n8.259 seconds\n```\n\n```text\ns4cmd get s3://fake-test-bucket/fake-prod-data/2020-10-17* --num-threads 100\n\nTimed out while listing objects after 60min.\n```\n\n#### With 8 threads\n```text\ns3fetch s3://fake-test-bucket/fake-prod-data/2020-10-17  --threads 8\n\n29.140 seconds\n```\n\n```text\ntime s4cmd get s3://fake-test-bucket/fake-prod-data/2020-10-17* --num-threads 8\n\nTimed out while listing objects after 60min.\n```\n\n## Installation\n\n### Requirements\n\n- Python >= 3.7\n- AWS credentials in one of the [standard locations](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html#cli-configure-files-where)\n\nS3Fetch is available on PyPi and can be installed via one of the following methods.\n\n### pipx (recommended)\n\nEnsure you have [pipx](https://pypi.org/project/pipx/) installed, then:\n\n`pipx install s3fetch`\n\n\n### pip\n\n`pip3 install s3fetch`\n\n\n## Usage:\n\n```\nUsage: s3fetch [OPTIONS] S3_URI\n\n  Easily download objects from an S3 bucket.\n\n  Example: s3fetch s3://my-test-bucket/birthday-photos/2020-01-01\n\n  The above will download all S3 objects located under the `birthday-\n  photos/2020-01-01` prefix.\n\n  You can download all objects in a bucket by using `s3fetch s3://my-test-\n  bucket/`\n\nOptions:\n  --region TEXT           Bucket region. Defaults to \'us-east-1\'.\n  -d, --debug             Enable debug output.\n  --download-dir TEXT     Download directory. Defaults to current directory.\n  -r, --regex TEXT        Filter list of available objects by regex.\n  -t, --threads INTEGER   Number of threads to use. Defaults to core count.\n  --dry-run, --list-only  List objects only, do not download.\n  --delimiter TEXT        Specify the "directory" delimiter. Defaults to \'/\'.\n  -q, --quiet             Don\'t print to stdout.\n  --version               Print out version information.\n  --help                  Show this message and exit.\n```\n\n## Examples:\n\n### Full example\n\nDownload using 100 threads into `~/Downloads/tmp`, only downloading objects that end in `.dmg`.\n\n```\n$ s3fetch s3://my-test-bucket --download-dir ~/Downloads/tmp/ --threads 100  --regex \'\\.dmg$\'\ntest-1.dmg...done\ntest-2.dmg...done\ntest-3.dmg...done\ntest-4.dmg...done\ntest-5.dmg...done\n```\n\n### Download all objects from a bucket\n\n```\ns3fetch s3://my-test-bucket/\n```\n\n### Download objects with a specific prefix \n\nDownload all objects that strt with `birthday-photos/2020-01-01`.\n```\ns3fetch s3://my-test-bucket/birthday-photos/2020-01-01\n```\n\n### Download objects to a specific directory\n\nDownload objects to the `~/Downloads` directory.\n```\ns3fetch s3://my-test-bucket/ --download-dir ~/Downloads\n```\n\n### Download multiple objects concurrently\n\nDownload 100 objects concurrently.\n```\ns3fetch s3://my-test-bucket/ --threads 100\n```\n\n### Filter objects using regular expressions\n\nDownload objects ending in `.dmg`.\n```\ns3fetch s3://my-test-bucket/ --regex \'\\.dmg$\'\n```\n\n',
    'author': 'Shane Anderson',
    'author_email': 'shane@reactivate.cx',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rxvt/s3fetch',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
