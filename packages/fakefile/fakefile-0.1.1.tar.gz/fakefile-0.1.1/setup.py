from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

setup(
    name='fakefile',
    url='https://github.com/anuvc/fakefile',
    version='0.1.1',
    description='Create fake files',
    long_description_content_type='text/markdown',
    long_description=readme,
    author="Anuv Chakraborty",
    author_email='anuv.chakrabo@gmail.com',
    license='Apache2',
    py_modules=['fakefile'],
    install_requires=[],
    keywords="fake corrupt file",
    entry_points='''
        [console_scripts]
        fakefile=fakefile:main
    ''',
)