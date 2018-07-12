# Copyright (c) 2015 Simon Kennedy <sffjunkie+code@gmail.com>

from setuptools import setup, find_packages

package_dir={'': 'src'}

setup(name='mogul',
    version="0.1",
    description="""mogul""",
#    long_description=open('README.txt').read(),
    author='Simon Kennedy',
    author_email='sffjunkie+code@gmail.com',
    url="http://www.sffjunkie.co.uk/python-mogul.html",
    license='Apache-2.0',
    
    install_requires=['beautifulsoup4', 'regex'],
    
    package_dir=package_dir,
    packages=find_packages(where=package_dir['']),
    namespace_packages=['mogul',],
)
