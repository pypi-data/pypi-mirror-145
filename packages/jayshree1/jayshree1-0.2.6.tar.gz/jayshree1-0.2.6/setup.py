from setuptools import setup

setup(
    name='jayshree1',
    version='0.2.6',
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
            'ad init = first:cli','ad run = first:run', 'ad seed = first:seed',
        ],
    },
)