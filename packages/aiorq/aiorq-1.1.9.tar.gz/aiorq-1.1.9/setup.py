from pathlib import Path

from importlib.machinery import SourceFileLoader
from setuptools import setup, find_packages

description = 'Job queues in python with asyncio and redis'
readme = Path(__file__).parent / 'README.md'
if readme.exists():
    long_description = readme.read_text()
else:
    long_description = description + '.\n\nSee https://readthedocs.org/projects/aiorq for documentation.'
# avoid loading the package before requirements are installed:
version = SourceFileLoader('version', 'aiorq/version.py').load_module()

setup(
    name='aiorq',
    version=version.__version__,
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Framework :: AsyncIO',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Clustering',
        'Topic :: System :: Distributed Computing',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Systems Administration',
    ],
    python_requires='>=3.7',
    author='PY-GZKY',
    author_email='341796767@qq.com',
    url='https://github.com/PY-GZKY/aiorq',
    license='MIT',
    packages=find_packages(),
    zip_safe=True,
    entry_points="""
        [console_scripts]
        aiorq=aiorq.cli:cli
    """,
    install_requires=[
        'aioredis>=2.0.0',
        'click>=6.7',
        'pydantic>=1',
        'dataclasses>=0.6;python_version == "3.8"',
        'typing-extensions>=3.7;python_version < "3.8"'
    ],
    extras_require={
        'watch': ['watchgod>=0.4'],
    }
)