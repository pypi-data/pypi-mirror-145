from setuptools import setup

setup(
    name='jayshree1',
    version='0.2.8',
    description = 'A small example package',
    long_description = open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    License= 'MIT',
    py_modules=['first'],
    python_requires='>=3.8, <4',
    install_requires=[
        'Click','pyDrive','requests','python-decouple','setuptools','pybtex','python-dotenv',
    ],
    entry_points={
        'console_scripts': [
            'init = first:cli','run = first:run', 'seed = first:seed',
        ],
    },
)