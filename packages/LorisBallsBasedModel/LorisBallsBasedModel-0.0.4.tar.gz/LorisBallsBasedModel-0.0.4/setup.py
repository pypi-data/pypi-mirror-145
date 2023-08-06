from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.4'
DESCRIPTION = 'A package that allows to build neural networks models using my balls.'

setup(
    name="LorisBallsBasedModel",
    version=VERSION,
    author="Loris Pilotto",
    author_email="loris.pilotto.pm@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['tensorflow',
                      'tensorflow-addons',
                      'keras-tuner',
                      'pandas',
                      'numpy'],
    keywords=['Python',
              'Neural Network',
              'TensorFlow',
              'LorisBallsBasedModel',
              'Machine Learning'],
    url='https://github.com/LorisPilotto/LorisBallsBasedModel',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)