from distutils.core import setup

setup(
    name='ceca-sorter',
    version='1.0',
    description='Python imports sorter written for Comparaencasa utilities',
    author='Martin Nieva',
    author_email='martinjafactor@gmail.com',
    packages=['ceca_sorter'],
    install_requires=('click', ),
    entry_points={
        'console_scripts': ['ceca-sorter=ceca_sorter.__main__:_main']
    }
)
