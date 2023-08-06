from setuptools import setup, find_packages


setup(
    name='mindturner',
    version='0.1',
    license='MIT',
    author="Computer Science Association",
    author_email='bitspcsa@gmail.com',
    packages=find_packages(),
    package_dir={'': 'mindturner/src'},
    keywords='mindturner answer',
    py_modules=["mindturner"],
    install_requires=[],
)