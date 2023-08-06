from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='wiz-feishu',

    version='2.0.2',

    description='wiz-feishu',

    long_description=long_description,

    long_description_content_type='text/markdown',

    url='https://chnyangjie.github.io/',

    author='chnyangjie',

    author_email='chnyangjie@gmail.com',

    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],

    keywords='python feishu client',
    package_dir={'wiz_feishu': 'src/wiz_feishu'},
    packages=find_packages(where='src'),
    python_requires='>=3.6, <4',
    install_requires=['requests', 'wiz-utils', 'wiz-message==2.0.5'],
    py_modules=['wiz_feishu'],
    project_urls={
        'Bug Reports': 'https://github.com/chnyangjie/wiz_feishu/issues',
        'Say Thanks!': 'https://github.com/chnyangjie/wiz_feishu/issues',
        'Source': 'https://github.com/chnyangjie/wiz_feishu',
    },
)
