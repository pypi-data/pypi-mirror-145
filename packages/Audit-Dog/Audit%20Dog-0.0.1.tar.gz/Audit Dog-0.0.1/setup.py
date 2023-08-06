from setuptools import setup

setup(
    name='Audit Dog',
    version='0.0.1',
    py_modules=['first'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'init = first:cli',
        ],
    },
)