from pathlib import Path
from setuptools import setup, find_packages

readme = Path('README.md').read_text()


setup(
    name='comgate',
    version='0.0.2',
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=[
        'requests'
    ],

    url='https://github.com/Salamek/comgate',
    license='LGPL-3',
    author='Adam Schubert',
    author_email='adam.schubert@sg1-game.net',
    description='Client library for comgate.cz payments',
    long_description=readme,
    long_description_content_type='text/markdown',
    test_suite='tests',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development',
    ],
    python_requires='>=3.4',
    project_urls={
        'Release notes': 'https://github.com/Salamek/comgate/releases',
    },
)
