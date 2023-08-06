from setuptools import setup, find_packages

__version__ = '1.0.2'

setup(
    name = 'pas-sdk-python3',
    install_requires = ['urllib3==1.26.4',],
    version = __version__,
    description = 'parametrix api service sdk for python3',
    long_description = 'parametrix api service sdk for python3',
    author = 'Chaocanshu',
    url = '',
    maintainer_email = '',
    scripts=[],
    packages = find_packages(exclude=["tests*"]),
    license="Apache License 2.0",
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
