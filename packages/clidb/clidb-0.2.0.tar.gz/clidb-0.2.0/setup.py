# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['clidb']

package_data = \
{'': ['*'],
 'clidb': ['.mypy_cache/*',
           '.mypy_cache/3.9/*',
           '.mypy_cache/3.9/_typeshed/*',
           '.mypy_cache/3.9/asyncio/*',
           '.mypy_cache/3.9/attr/*',
           '.mypy_cache/3.9/clidb/*',
           '.mypy_cache/3.9/collections/*',
           '.mypy_cache/3.9/concurrent/*',
           '.mypy_cache/3.9/concurrent/futures/*',
           '.mypy_cache/3.9/ctypes/*',
           '.mypy_cache/3.9/duckdb/*',
           '.mypy_cache/3.9/email/*',
           '.mypy_cache/3.9/html/*',
           '.mypy_cache/3.9/importlib/*',
           '.mypy_cache/3.9/importlib/metadata/*',
           '.mypy_cache/3.9/json/*',
           '.mypy_cache/3.9/logging/*',
           '.mypy_cache/3.9/multiprocessing/*',
           '.mypy_cache/3.9/os/*',
           '.mypy_cache/3.9/rich/*',
           '.mypy_cache/3.9/textual/*',
           '.mypy_cache/3.9/textual/drivers/*',
           '.mypy_cache/3.9/textual/layouts/*',
           '.mypy_cache/3.9/textual/views/*',
           '.mypy_cache/3.9/textual/widgets/*',
           '.mypy_cache/3.9/urllib/*',
           '.mypy_cache/3.9/uvloop/*',
           '.mypy_cache/3.9/uvloop/includes/*']}

install_requires = \
['duckdb>=0.3.2,<0.4.0',
 'textual-inputs>=0.2.0,<0.3.0',
 'textual>=0.1.0,<0.2.0']

extras_require = \
{'extras': ['pandas>=1.3,<2.0',
            'pyarrow>=7.0.0,<8.0.0',
            'fsspec>=2022.2.0,<2023.0.0',
            'boto3>=1.20,<2.0',
            's3fs>=2022.2.0,<2023.0.0',
            'xlrd>=2.0.1,<3.0.0']}

entry_points = \
{'console_scripts': ['clidb = clidb.cli:CliDB.run']}

setup_kwargs = {
    'name': 'clidb',
    'version': '0.2.0',
    'description': 'CLI based SQL client for local data',
    'long_description': '# clidb\n\n![screenshot](./img/iris.png)\n\nclidb is a command line sql client for individual data files, allowing these to be queried (even joined) and viewed. It natively supports CSV and parquet formats, with support for other file types available via the optional extras dependency.\n\n## Data Formats\nThe following file types can be opened as views in clidb without extras:\n- csv\n- parquet(.gz)\n\nWith pandas installed, the following are also supported:\n- json(l)\n- xls(x)\n- clipboard\n- ...\n\n## Usage\n\nThis package can be installed with:\n\n```bash\npip install "clidb[extras]"\n```\n\nand executed via:\n\n```bash\nclidb\n```\n\n### Arguments\n\nIf a filename is supplied as an argument to clidb then it will open the data file as a view.\n\nIf a directory or S3 path is supplied then the directory view will open in that location.\n\nFor example:\n\n```bash\nclidb data/iris.csv\n```\n\nor\n\n```bash\nclidb s3://somebucket/data/\n```\n\nThe contents of the clipboard can be converted into a view (e.g. after copying from Google Sheets), using the `--clipboard` argument:\n\n```bash\nclidb --clipboard\n```\n\nFor some data sources, it can be helpful to render lines that separate rows. This can be enabled via the `row-lines` option:\n\n```bash\nclidb --row-lines\n```\n\n## Advanced Usage\nNew views can be created from an opened file. For example if `iris.csv` was opened as the view `iris`, then we could create a new view:\n```sql\ncreate view iris_variety as (select variety, avg("petal.length") from iris group by variety)\n```\n\n![create view](./img/iris_variety.png)\n\nViews can be joined together, for example:\n```sql\nselect * from iris natural join iris_variety\n```\n\n![join](./img/iris_join.png)\n',
    'author': 'Danny Boland',
    'author_email': 'danny@boland.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dannyboland/clidb',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
