from setuptools import setup, find_packages


setup(
    name='csa-mindturner',
    version='0.4',
    license='MIT',
    author="Computer Science Association",
    author_email='bitspcsa@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    keywords='mindturner answer',
    py_modules=["csa_mindturner"],
    install_requires=[],
)