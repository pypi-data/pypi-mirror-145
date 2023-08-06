from setuptools import setup

setup(
    name='fakefile',
    version='0.1.0',
    py_modules=['fakefile'],
    install_requires=[],
    entry_points='''
        [console_scripts]
        fakefile=fakefile:main
    ''',
)