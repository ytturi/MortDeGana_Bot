from setuptools import setup, find_packages


setup(
    name='meldebot',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        "click",
        "python-telegram-bot",
        "ConfigParser",
        "requests",
    ],
    entry_points='''
        [console_scripts]
        meldebot=meldebot.meldebot:listener
    ''',
)
