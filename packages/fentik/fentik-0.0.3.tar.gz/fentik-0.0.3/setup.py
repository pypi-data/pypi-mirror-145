from setuptools import setup

setup(
    name='fentik',
    version='0.0.3',
    author="Fentik, Inc.",
    author_email="support@fentik.com",
    description="Real-time data platform for in product experiences",
    url="https://github.com/fentik/fentik-cli",
    packages=['fentik'],
    scripts=['scripts/fentik'],
    install_requires=[
        'PrettyTable',
        'graphqlclient',
	'PyYAML',
    ],
)
