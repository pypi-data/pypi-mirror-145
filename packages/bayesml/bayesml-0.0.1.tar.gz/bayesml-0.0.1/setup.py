from setuptools import setup, find_packages

setup(
    name='bayesml',
    version='0.0.1',
    packages=find_packages(),
    author='Yuta Nakahara et al.',
    author_email='yuta.nakahara@aoni.waseda.jp',
    url='https://twitter.com/bayesml',
    description='A library for Bayes statistics, Bayes decision theory, and Bayes machine learning',
    long_description=open('README.md').read(),
    classifiers=['Development Status :: 2 - Pre-Alpha',
                 'License :: OSI Approved :: BSD License'],
)