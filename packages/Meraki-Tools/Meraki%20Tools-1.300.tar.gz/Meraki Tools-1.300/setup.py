
"""
setup for click
"""
from setuptools import setup,find_packages
req = ['aiohttp','async-timeout','attrs','bcolors',
'certifi','chardet','idna','meraki','multidict','requests',
'typing-extensions','urllib3','yarl','http3','click','pandas',
'tabulate','python-dateutil','automodinit','python-dotenv','wheel',"deepdiff","jsonpickle","viptela","flask","werkzeug",
       "flask-restful"]
setup(
    name='Meraki Tools',
    version='1.300',
    author='Josh Lipton',
    author_email='joliptn@cisco.com',
    description='CLI tool to manage multipal meraki orginizations',
	packages=find_packages(),
    packages_data=['merakitools'],
    include_package_data=True,
	install_requires=[req],
    entry_points="""
        [console_scripts]
        merakitools=merakitools.cli.cli:cli
    """,
)
