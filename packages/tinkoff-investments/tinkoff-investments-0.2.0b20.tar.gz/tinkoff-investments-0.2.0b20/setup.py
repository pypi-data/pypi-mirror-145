# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tinkoff',
 'tinkoff.invest',
 'tinkoff.invest.grpc',
 'tinkoff.invest.market_data_stream']

package_data = \
{'': ['*']}

install_requires = \
['grpcio>=1.39.0,<2.0.0', 'protobuf>=3.19.3,<4.0.0', 'tinkoff>=0.1.1,<0.2.0']

setup_kwargs = {
    'name': 'tinkoff-investments',
    'version': '0.2.0b20',
    'description': '',
    'long_description': '# Tinkoff Invest\n\n[![PyPI](https://img.shields.io/pypi/v/tinkoff-investments)](https://pypi.org/project/tinkoff-investments/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tinkoff-investments)](https://www.python.org/downloads/)\n\nДанный репозиторий предоставляет клиент для взаимодействия с торговой платформой [Тинькофф Инвестиции](https://www.tinkoff.ru/invest/) на языке Python.\n\n- [Документация](https://tinkoff.github.io/invest-python/)\n- [Основной репозиторий с документацией](https://github.com/Tinkoff/investAPI)\n- [Документация для разработчиков](https://tinkoff.github.io/investAPI/)\n\n## Начало работы\n\n<!-- termynal -->\n\n```\n$ pip install tinkoff-investments\n```\n\n## Возможности\n\n- &#9745; Синхронный и асинхронный GRPC клиент\n- &#9745; Возможность отменить все заявки\n- &#9745; Выгрузка истории котировок "от" и "до"\n- &#9744; Кеширование данных\n- &#9744; Торговая стратегия\n\n## Примеры\n\nПримеры доступны [здесь](https://github.com/Tinkoff/invest-python/tree/main/examples).\n\n```python\nfrom tinkoff.invest import Client\nfrom tinkoff.invest.token import TOKEN\n\nwith Client(TOKEN) as client:\n    print(client.users.get_accounts())\n```\n\nДля запуска примеров, нужно добавить токен в переменную окружения.\n\n<!-- termynal -->\n\n```\n$ export INVEST_TOKEN=YOUR_TOKEN\n```\n\n## Contribution\n\n- [CONTRIBUTING](https://github.com/Tinkoff/invest-python/blob/main/CONTRIBUTING.md)\n\n## License\n\nЛицензия [The Apache License](https://github.com/Tinkoff/invest-python/blob/main/LICENSE).\n',
    'author': 'Danil Akhtarov',
    'author_email': 'd.akhtarov@tinkoff.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Tinkoff/invest-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
