try:
    from setuptools import setup
except ImportError:
    from disutils.core import setup

config={
    'description': 'Welcome Home',
    'author': 'Jiaming Yi',
    'url': 'URL to get it at.',
    'download_url': 'Where to download it.',
    'author_email': 'mingtian3229/*@*/hotmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['welcomehome'],
    'scripts': [],
    'name': 'welcome home'
}

setup(**config)