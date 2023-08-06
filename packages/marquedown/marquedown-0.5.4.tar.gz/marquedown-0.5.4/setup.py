# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['marquedown', 'marquedown.commands']

package_data = \
{'': ['*']}

install_requires = \
['Markdown>=3.3.6,<4.0.0', 'PyYAML>=6.0,<7.0']

setup_kwargs = {
    'name': 'marquedown',
    'version': '0.5.4',
    'description': 'Extending Markdown further by adding a few more useful notations.',
    'long_description': '# Marquedown\n\nExtending Markdown further by adding a few more useful notations.\nIt can be used in place of `markdown` as it also uses and applies it.\n\n## Examples\n\n### Blockquote with citation\n\nThis is currently limited to the top scope with no indentation.\nSurrounding dotted lines are optional.\n\n```md\n......................................................\n> You have enemies? Good. That means you\'ve stood up\n> for something, sometime in your life.\n-- Winston Churchill\n\'\'\'\'\'\'\'\'\'\'\'\'\'\'\'\'\'\'\'\'\'\'\'\'\'\'\'\'\'\'\'\'\'\'\'\'\'\'\'\'\'\'\'\'\'\'\'\'\'\'\'\'\'\'\n```\n\n```html\n<blockquote>\n    <p>\n        You have enemies? Good. That means you\'ve stood up\n        for something, sometime in your life.\n    </p>\n    <cite>Winston Churchill</cite>\n</blockquote>\n```\n\n### Embed video\n\n#### YouTube\n\n```md\n![dimweb](https://youtu.be/VmAEkV5AYSQ "An embedded YouTube video")\n```\n\n```html\n<iframe\n    src="https://www.youtube.com/embed/VmAEkV5AYSQ"\n    title="An embedded YouTube video" frameborder="0"\n    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"\n    allowfullscreen>\n</iframe>\n```\n\n## Commands\n\n### `render`: Render documents\n\nYou can render an entire directory and its subdirectories of Markdown or Marquedown documents. This can be used to automate rendering pages for your website.\n\nDo `python -m marquedown render --help` for list of options.\n\n#### Example\n\nFor a few of my websites hosted on GitLab, I have it set up to run *this* on push:\n\n```sh\n# Render document\npython -m marquedown render -i ./md -o ./public -t ./templates/page.html\n\n# This is for the GitLab Pages publication\nmkdir .public\ncp -r public .public\nmv .public public  \n```',
    'author': 'Maximillian Strand',
    'author_email': 'maximillian.strand@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/deepadmax/marquedown',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
