from setuptools import find_packages, setup

with open("dev_requirements.txt", "r") as dev_deps:
    test_deps = [dep.strip() for dep in dev_deps.readlines() if dep.strip()]

setup(
    name="meldebot",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "click",
        "python-telegram-bot",
        "ConfigParser",
        "requests",
        "sqlalchemy",
        "psycopg2-binary",
    ],
    entry_points="""
        [console_scripts]
        meldebot=meldebot.bot:listener
    """,
    # tests_require=test_deps,
    tests_suite="spec",
)
