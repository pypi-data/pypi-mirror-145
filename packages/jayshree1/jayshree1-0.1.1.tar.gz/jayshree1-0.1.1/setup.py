from setuptools import setup

setup(
    name='jayshree1',
    version='0.1.1',
    description = 'A small example package',
    long_description = open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    License= 'MIT',
    py_modules=['first'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'init = first:cli','run = first:run',
        ],
    },
)