#!/usr/bin/env python3

from distutils.core import setup

setup(
    name='njupy',
    version='0.1.0',
    description='An easy to use sort of front end for  untitled-ai/jupyter_ascending.vim ',
    url='https://github.com/goncalogiga/njupy',
    author='Gonçalo Giga',
    author_email='',
    license='',
    packages=['njupy'],
    install_requires=['jupyter_ascending',
                      'jupytext',
                      'click',
                      ],
    scripts=['bin/njupy']
)
