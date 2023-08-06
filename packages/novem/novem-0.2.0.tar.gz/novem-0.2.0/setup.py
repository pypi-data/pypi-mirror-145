# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['novem', 'novem.cli', 'novem.vis']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0']

entry_points = \
{'console_scripts': ['novem = novem.cli:run_cli']}

setup_kwargs = {
    'name': 'novem',
    'version': '0.2.0',
    'description': 'python library for the novem.no data visualisation platform',
    'long_description': '\n# novem - data visualisation for coders\n\nA wrapper library for the novem.no data visualisation platform. Create charts,\ndocuments e-mails and dashboards through one simple api.\n\n**NB:** novem is currently in closed alpha, if you want to try it out please\nreach out to hello@novem.no\n\n\n## Exampels\n\nCreate a linechart from a dataframe using pandas data reader\n\n```python\nfrom pandas_datareader import data\nfrom novem import Plot\n\nline = Plot("aapl_price_hist", type="line", name="Apple price history")\n\n# Only get the adjusted close.\naapl = data.DataReader("AAPL",\n                       start="2015-1-1",\n                       end="2021-12-31",\n                       data_source="yahoo")["Adj Close"]\n\n# send data to the plot\naapl.pipe(line)\n\n# url to view plot\nprint(line.url)\n```\n\n\n## Getting started\nTo get started with novem you\'ll have to register an account, currently this\ncan be done by reaching out to the novem developers on hello@novem.no.\n\nOnce you have a username and password you can setup your environment using:\n```bash\n  python -m novem --init\n```\n\nIn additon to invoking the novem module as shown above, the novem package also\nincludes an extensive command-line interface (cli). Check out CLI.md in this\nrepostiory or [novem.no](https://novem.no) for more details.\n\n\n\n## Creating a plot\nNovem represents plots as a Plot class that can be imported from the main novem\npackage `from novem import Plot`.\n\nThe plot class takes a single mandatory positional argument, the name of the\nplot.\n * If the plot name is new, the instantiation of the class will create the plot.\n * If the plot name already exist, then the new object will operate on the\n   existing plot.\n\nIn addition to the name, there are two broad categories of options for a\nplot, data and config:\n * The **data** contains the actual information to visualise (usually in the form\n   of numeric csv)\n * **Config**, which contains information about the visual such as:\n   * Type (bar, line, donut, map etc)\n   * Titles/captions/names/colors/legends/axis etc\n\n\nThere are two ways to interact with the plots, one can either supply all\nthe neccessary options as named arguments when creating the plot, or use the\nproperty accessors to modfity them one by one (this is more helpful when working\nwith the plot in an interactive way). Below is an example of the two\napproaches.\n\n```python\nfrom novem import Plot\n\n# everything in the constructor\nbarchart = Plot(<name>, \\\n  type="bar", \\\n  title="barchart title", \\\n  caption = "caption"\n)\n\n# property approach\nbarchart = Plot("plot_name")\nbarchart.type = "bar"\nbarchart.title = "barchart title"\nbarchart.caption = "caption"\n```\n\nIn addition to setting individual properties, the plot object is also callable.\nThis means that the resulting plot can be used as a function, either by being\nprovided data as an argument, or used as part of a pipe chain.\n\n```python\nfrom novem import Plot\nimport pandas as pd\nimport numpy as np\n\n# construct some random sample data\ndf = pd.DataFrame(np.random.randn(100, 4), columns=list("ABCD")).cumsum()\n\nline = Plot("new_line", type="line")\n\n# alternative one, setting data explicitly to a csv string\nline.data = df.to_csv()\n\n# or let the plot invoke the to_csv\nline.data = df\n\n# alternative two, calling Plot with a csv string\nline(df.to_csv())\n\n# alternative three calling the Plot with an object that has a to_csv function\nline(df)\n\n# or\ndf.pipe(line)\n\n```\n\n\n**NB:** All novem plot operations are live.\nThis means that as soon as you write to or modify any aspects of the plot\nobject, those changes are reflected on the novem server and anyone watching\nthe plot in real time.\n\n\n\n## Contribution and development\nThe novem python library and platform is under active development, contributions\nor issues are most welcome.\n\nFor guidelines on how to contribute, please check out the CONTRIBUTING.md file\nin this repository.\n\n\n## LICENSE\nThis python library is licensed under the MIT license, see the LICENSE file for\ndetails\n',
    'author': 'Sondov Engen',
    'author_email': 'sondov@novem.no',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://novem.no',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
