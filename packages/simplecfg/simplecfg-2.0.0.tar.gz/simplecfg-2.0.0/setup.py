from setuptools import setup
import simplecfg

with open("README.md", "r") as fh:
	long_description = fh.read()

setup(
	name=simplecfg.MODULE_NAME,
	version=simplecfg.MODULE_VERSION,
	packages=[simplecfg.MODULE_NAME],
	url=simplecfg.MODULE_URL,
	license="MIT License",
	author=simplecfg.MODULE_AUTHOR,
	author_email="max.loiacono@protonmail.com",
	description=simplecfg.MODULE_DESCRIPTION,
	long_description=long_description,
	long_description_content_type="text/markdown",
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires=">=3.3"
)
