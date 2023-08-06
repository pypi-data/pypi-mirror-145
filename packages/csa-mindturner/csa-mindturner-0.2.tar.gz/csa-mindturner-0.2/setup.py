from setuptools import setup, find_packages


setup(
    name='csa-mindturner',
    version='0.2',
    license='MIT',
    author="Computer Science Association",
    author_email='bitspcsa@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    keywords='mindturner answer',
    install_requires=[],
)