import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
	long_description = fh.read()

setuptools.setup(
	name="pymaid",
	version="dev",
	author="David Losantos (DarviL82)",
	author_email="davidlosantos89@gmail.com",
	description="Generate a mermaid representation from Python code.",
	long_description=long_description,
	long_description_content_type="text/markdown",
	project_urls={
		"Tracker": "https://github.com/DarviL82/pymaid/issues",
	},
	classifiers=[
		"Programming Language :: Python :: 3.10",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	package_dir={"": "src"},
	packages=setuptools.find_packages(where="src"),
	python_requires=">=3.10",
	entry_points={
		"console_scripts": [
			"pymaid=pymaid"
		]
	}
)
