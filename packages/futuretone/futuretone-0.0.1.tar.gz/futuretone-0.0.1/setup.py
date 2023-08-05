from setuptools import setup, find_packages


setup(
    name='futuretone',
    version='0.0.1',
    author='Jay',
    author_email='0jaybae0@gmail.com',
    description='Integrates into Future Tone on the PS4',
    url='https://github.com/Jay184/FT-Unofficial/tree/dev/api',
    project_urls={
        'Bug Tracker': 'https://github.com/Jay184/FT-Unofficial/labels/api',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    py_modules=['futuretone'],
    include_package_data=True,
    entry_points='''
        [console_scripts]
        futuretone=futuretone:app
    ''',
    install_requires=[
        'click<8.1.0',
        'aiohttp==3.8.1',
        'aiosignal==1.2.0',
        'async-timeout==4.0.2',
        'attrs==21.4.0',
        'charset-normalizer==2.0.12',
        'colorama==0.4.4',
        'frozenlist==1.3.0',
        'idna==3.3',
        'iso8601==1.0.2',
        'multidict==6.0.2',
        'twitchio==2.2.0',
        'typer==0.4.0',
        'typing_extensions==4.1.1',
        'yarl==1.7.2',
        'ps4debug', # Hey, I made this one! Check it out at "https://pypi.org/project/ps4debug/"
    ],
    python_requires='>=3.10'
)
