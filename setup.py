from setuptools import setup

setup(
    name='everyailment',
    version='0.1.dev',
    py_modules=['everyailment'],
    package_data={'': ['data/ailments.json']},
    install_requires=[
        'Click',
        'twython',
    ],
    entry_points="""
        [console_scripts]
        everyailment=everyailment:cli
    """,
)
