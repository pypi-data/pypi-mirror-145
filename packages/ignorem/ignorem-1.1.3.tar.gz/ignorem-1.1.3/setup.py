from setuptools import setup
import ignorem

with open("README.md", "r") as fh:
	long_description = fh.read()

setup(
	name=ignorem.PROGRAM_NAME,
	version=ignorem.PROGRAM_VERSION,
	packages=['ignorem'],
	url=ignorem.PROGRAM_URL,
	license='MIT License',
	author=ignorem.PROGRAM_AUTHOR,
	author_email='',
	description=ignorem.PROGRAM_DESCRIPTION,
	long_description=long_description,
	long_description_content_type="text/markdown",
	entry_points={
		'console_scripts': ['ignorem=ignorem:_main']
	},
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	install_requires=[
		"simplecfg < 2.0.0"
	],
	python_requires='>=3.6'
)
