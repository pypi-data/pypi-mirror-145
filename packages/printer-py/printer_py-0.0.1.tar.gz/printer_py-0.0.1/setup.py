from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'A printer package helps you to debug using print any number of variables of any types only with comma.'

# Setting up
setup(
    name="printer_py",
    version=VERSION,
    author="Ninad Goswamy (ninsgosai)",
    author_email="<ninad.goswamy@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'debug', 'print', 'diffrent type value', 'python debug', 'python2','printer_py','printer-py'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)