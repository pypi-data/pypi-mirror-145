from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "pyjjasim/README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '4.0.0'
DESCRIPTION = 'Circuit Simulator including Josephson Junctions in Python'
LONG_DESCRIPTION = 'PyJJASim is a circuit simulator including Josephson Junctions as components, intended ' \
                   'to be used on large Josephson Junction Arrays (JJAs). PyJJASim is specialized in keeping track ' \
                   'of Josephson vortices in the circuit. It can also compute static configurations that have ' \
                   'vortices at desired locations in the circuit.'

# Setting up
setup(
    name="pyjjasim",
    version=VERSION,
    author="Martijn Lankhorst",
    author_email="<m.lankhorst89@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['numpy', 'scipy', 'matplotlib'],
    keywords=['python', 'josephson_junction_array', 'circuit', 'simulation'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)