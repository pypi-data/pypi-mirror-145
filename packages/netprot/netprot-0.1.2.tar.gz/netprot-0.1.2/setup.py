# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['netprot']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'netprot',
    'version': '0.1.2',
    'description': 'A system-indipendent network protocol manipulation and evaluation library.',
    'long_description': "# netprot\nA system-independent network protocol manipulation and evaluation library. `netprod` wants to be a library capable of standardizing and evaluating a list of strings representing Network Protocols. The idea is to provide a tool similar to netaddr that can help to enhance and simplify code logic wherever is required.\n\n### Installation\n\n```bash\npip3 install netprod\n```\n\nPackage available [here](https://pypi.org/project/netprot/)\n\n### HOW TO\n\nFirst thing, we need to initialize an instance of `Netprod` class, passing as arguments a list of strings - where each string should represent a network protocol and corresponding port. A `separator` argument is also possible to pass as kwarg and will be used to standardize our strings. By default, separator is equal to `/`\n\n```python\n>>> from netprot.netprot import Netprot \n>>> my_list = ['tcp-443-https', 'UDP/53', 'tcp/1024-1026', 'TCPP-80', 'tcp/443']\n>>> my_protocols = Netprot(my_list, exceptions=['ICMP', 'any'], separator='/')\n```\n\nOnce the instance of the class is created, we can call `standardize` method which will return a tuple containing pontential unlegal protocols and ports, duplicates - if any, and a standardize list of protocols and port.\n\n```python\n>>> my_protocols.standardize()\n(['TCPP/80'], ['TCP/443'], ['ANY', 'ICMP', 'TCP/1024', 'TCP/1025', 'TCP/1026', 'TCP/443', 'UDP/53'])\n```\n\nAs we can see, we have:\n\n- Strings using the same `separator`.\n- Trailing words such as `https` is removed as not needed\n- Protocols defined as `tcp/1024-1026` are unpacked for each port in range defined\n- Illegal protocols such as TCPP/80 are removed\n- Duplicates are also removed\n- All strings are upper cases\n- List is sorted\n- `ICMP` and `ANY` are recognized as legal - because defined under `exceptions` argument - and passed through\n\n\n`Netprod` not only standardizes data, but also evaluates them. Let's have a look to the other methods\n\n:warning:\nList of protocols must be standardized first.\n\nLet's check if the ports are part of well known range of ports (0 to 1024)\n\n```python\n>>> my_protocols.is_well_known()\n(False, [False, False, True, False, False, True, True])\n```\n\nAs we can see, some ports are failing to be lower than 1024, hence we return `False` plus a list of bools for each ports.\n\nWhat about if we want to find those are `TCP`...\n\n```python\n>>> my_protocols.is_tcp()\n(False, [False, False, True, True, True, True, False])\n```\n\n... or `UDP`?\n```python\n>>> my_protocols.is_udp()\n(False, [False, False, False, False, False, False, True])\n```\n\nGreat! What if we want figure out if our port and protocols are safe or not?\nLet's define a list of safe - or unsafe - ports and protocols and passed them to `is_safe` or `is_unsafe` method.\n\n```python\n>>> my_safe_applications = ['TCP/443', 'UDP/53']\n>>> my_protocols.is_safe(my_safe_applications)\n[False, False, False, False, False, True, True]\n>>> my_unsafe_applications = ['ICMP', 'ANY']\n>>> my_protocols.is_unsafe(my_unsafe_applications)\n[True, True, False, False, False, False, False]\n```\n\nAnd that's all, folks!\n",
    'author': 'Federico Olivieri',
    'author_email': 'lvrfrc87@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lvrfrc87/netprot',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
