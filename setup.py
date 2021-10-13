import sys

from functools import partial

from setuptools import find_packages, setup

utf_read = partial(open, mode='r', encoding='utf-8')

with utf_read('README.md') as f:
    readme = f.read()
with utf_read('LICENSE') as f:
    lcs = f.read()
info = sys.version_info
setup(
    name='otsumorsecode',
    version='1.0.1',
    url='https://github.com/Otsuhachi/OtsuMorseCode',
    description='[Windows Only!]英数字と一部記号で構成された文字列とモールス信号表現を相互変換します。また、音を再生します。',
    long_description_content_type='text/markdown',
    long_description=readme,
    author='Otsuhachi',
    author_email='agequodagis.tufuiegoeris@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 1 - Planning', 'Natural Language :: Japanese', 'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8', 'Programming Language :: Python :: 3.9', 'Operating System :: Microsoft :: Windows :: Windows 10',
        'License :: OSI Approved :: MIT License'
    ],
    license=lcs,
    keywords='Python Python3 morse_code モールス信号',
    install_requires=[
        'otsuvalidator',
    ],
)
