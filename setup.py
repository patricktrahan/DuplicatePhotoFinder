from setuptools import setup

APP = ['DuplicatePhotoFinder.py']
OPTIONS = {
    'argv_emulation': True,
    'packages': ['PIL'],
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)