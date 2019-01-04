from distutils.core import setup

from setuptools import find_packages

setup(
    name='pytoolz',
    version='0.1dev',
    packages=find_packages(),
    # packages=['pytoolz'],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description="",
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)

# packages=[
#         'src.design',
#         'src.ds',
#         'src.log',
#         'src.multiprocessing'
#         ],
