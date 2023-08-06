from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'A very basic calutor.'
LONG_DESCRIPTION = open('README.txt').read()+'\n\n'+open('CHANGELOG.txt').read()


classifiers= [
	"Development Status :: 5 - Production/Stable",
	"Intended Audience :: Education",
	"Programming Language :: Python :: 3",
	"Operating System :: Microsoft :: Windows :: Windows 10",
	"License :: OSI Approved :: MIT License"
]



# Setting up
setup(
	name="ANbasicCalculator", 
	version=VERSION,
	author="Ayan",
	author_email="ayanU881@gmail.com",
	license='MIT',
	classifiers = classifiers,
	description=DESCRIPTION,
	long_description=LONG_DESCRIPTION,
	packages=find_packages(),
	install_requires=[''], # add any additional packages that 
	keywords=['python', 'calculator'],
       
)