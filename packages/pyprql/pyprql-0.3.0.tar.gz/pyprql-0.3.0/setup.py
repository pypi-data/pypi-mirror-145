# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyprql', 'pyprql.cli', 'pyprql.lang']

package_data = \
{'': ['*'], 'pyprql': ['assets/*']}

install_requires = \
['Pygments>=2.11.2,<3.0.0',
 'SQLAlchemy>=1.4.32,<2.0.0',
 'click>=8.0.4,<9.0.0',
 'enforce-typing>=1.0.0,<2.0.0',
 'fuzzyfinder>=2.1.0,<3.0.0',
 'icecream>=2.1.2,<3.0.0',
 'lark>=1.1.2,<2.0.0',
 'prompt-toolkit>=3.0.28,<4.0.0',
 'rich>=12.0.0,<13.0.0']

entry_points = \
{'console_scripts': ['pyprql = pyprql.cli.cli:main']}

setup_kwargs = {
    'name': 'pyprql',
    'version': '0.3.0',
    'description': 'Python Implementation of Pipelined Relational Query Language (PRQL)',
    'long_description': '# PyPrql\n\nPython implementation of [PRQL](https://github.com/max-sixty/prql).\n\nDocumentation of PRQL is at https://github.com/max-sixty/prql\n\n### Installation\n```\n    pip install pyprql\n```\n\n## CLI\n\nUsage:\n\n```bash\n    pyprql \'connection_string\'\n    pyprql \'postgresql://user:password@localhost:5432/database\'    \n```\nExamples:\n\n```bash\n    pyprql \'sqlite:///chinook.db\'\n```\nTry it out:\n\n```\ncurl https://github.com/qorrect/PyPrql/blob/main/resources/chinook.db?raw=true -o chinook.db \npyprql "sqlite:///chinook.db"\n\nPRQL> show tables \n```\n\n## pyprql.to_sql \n\n```elm\nquery=\'\'\'\nfrom employees\nfilter country = "USA"\nderive [\n  gross_salary: salary + payroll_tax,\n  gross_cost:   gross_salary + benefits_cost\n]\nfilter gross_cost > 0\naggregate by:[title, country] [\n    average salary,\n    sum     salary,\n    average gross_salary,\n    sum     gross_salary,\n    average gross_cost,\n    sum_gross_cost: sum gross_cost,\n    row_count: count salary\n]\nsort sum_gross_cost\nfilter row_count > 200\ntake 20\n\'\'\'\n```\n\n---\n\n```python\n\nfrom pyprql import to_sql\nsql = to_sql(query)\nprint(sql)\n```\n\n---\n\n```sql\nSELECT AVG(salary),\n       SUM(salary),\n       AVG(salary + payroll_tax),\n       SUM(salary + payroll_tax),\n       AVG(salary + payroll_tax + benefits_cost),\n       SUM(salary + payroll_tax + benefits_cost) as sum_gross_cost,\n       COUNT(salary)                             as row_count,\n       salary + payroll_tax                      as gross_salary,\n       (salary + payroll_tax) + benefits_cost    as gross_cost\nFROM `employees` employees_e\nWHERE country="USA" AND (gross_salary+benefits_cost)>0\nGROUP BY title, country\nHAVING row_count >200\nORDER BY sum_gross_cost\nLIMIT 20\n\n```\n\n#### Differences from the spec\n\nThe parser is only able to parse casts in select statements insde of `[ ]`, so\n\n```sql\nselect foo | as float\n```\n\nwill fail, it must be wrapped in brackets as a single item list.\n\n```sql\nselect [ foo | as float ]\n```\n',
    'author': 'qorrect',
    'author_email': 'charlie.fats@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/qorrect/PyPrql',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
