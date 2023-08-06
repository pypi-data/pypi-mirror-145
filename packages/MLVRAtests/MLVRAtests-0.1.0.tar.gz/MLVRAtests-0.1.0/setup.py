# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')


setup(
    
    name='MLVRAtests',  
    version='0.1.0',  
    description='Set of tools to measure and test for violations of the 1982 Voting Rights Amendment', 
    long_description=long_description, 
    long_description_content_type='text/markdown', 
    url='',  
    author='Robert Edwardes',  
    author_email='robie@fairlines.org',  
    classifiers=[  
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "Programming Language :: Python :: 3.10",
        'Programming Language :: Python :: 3 :: Only',
    ],
    packages=find_packages(where='src'), 
    python_requires='>=3.6, <4',
    install_requires=['pandas','pymc3','seaborn','matplotlib','sklearn','shapely','geopandas','numpy'], 
    package_dir={'': 'src'},
)