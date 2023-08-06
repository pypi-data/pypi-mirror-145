from pydisco import __version__
from setuptools import setup

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

readme = ''
with open('README.md') as f:
    readme = f.read()

setup(
    name='pydiscoo',
    author='Pelfox',
    author_email='me@pelfox.dev',
    url='https://github.com/Pelfox/pydisco',
    version=__version__,
    packages=[
        'pydisco'
    ],
    license='MIT',
    description='Another Discord Wrapper for Python. Simplified and powerful bots are here.',
    long_description=readme,
    long_description_content_type='text/markdown',
    include_package_data=True,
    install_requires=requirements,
    python_requires='>=3.8.0',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
