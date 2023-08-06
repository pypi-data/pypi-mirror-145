from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.3'
DESCRIPTION = 'This is a python module in which you can store a csv file data and perform basic SQL features '
LONG_DESCRIPTION = '''
This module is made by Mainak Deb, this is a python module in which you can fetch CSV file data
and perform basic SQL operations in it.
        Features:
             1> Fetch csv
             2> Show in command prompt
             3> select
             4> projection
             5> update
             6> delete 
             7> order by
             8> group by
             9> access
            10> insert
            11> count
            12> sum
            13> max
            14> avarage
            15> pie chart
            16> histogram
            17> self join
            18> cross join
'''

# Setting up
setup(
    name="tablecsv",
    version=VERSION,
    author="mainakdeb",
    author_email="mainakdeb01@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy==1.22.2' ,'matplotlib==3.5.1' ],
    keywords=['arithmetic', 'math', 'mathematics', 'python tutorial', 'mainak deb',
    'excel','csv','dbms','sql','data','data science','python','table','oracledb','mysql',
    'pattern','pie','hiostogram','join','graph','fetch','data visualization'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)