from setuptools import setup

setup(
    name='jurn',
    version='0.1.0',
    py_modules=['jurn'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'jurn = src.jurn.main:cli',
        ],
    },
)