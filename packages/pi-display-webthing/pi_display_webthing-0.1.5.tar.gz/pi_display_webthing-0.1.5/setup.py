from setuptools import setup
from os import path


PACKAGENAME = 'pi_display_webthing'
ENTRY_POINT = "display"
DESCRIPTION = "A web connected LCD display module"


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name=PACKAGENAME,
    packages=['pi_display_webthing'],
    version_config={
        "version_format": "{tag}.dev{sha}",
        "starting_version": "0.0.1"
    },
    setup_requires=['better-setuptools-git-version'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    author='Gregor Roth',
    author_email='gregor.roth@web.de',
    url='https://github.com/grro/pi_display_webthing',
    entry_points={
        'console_scripts': [
            ENTRY_POINT + '=' + PACKAGENAME +':main'
        ]
    },
    keywords=[
        'webthing', 'LCD', 'display', 'home automation', 'raspberry', 'pi'
    ],
    install_requires=[
        'webthing==0.15.0',
        'smbus2',
        'RPLCD'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha"
    ],
)

