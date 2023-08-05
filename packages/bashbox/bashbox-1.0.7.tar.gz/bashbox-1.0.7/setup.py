import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bashbox",
    version="1.0.7",
    author="Bash Elliott",
    author_email="spicethings9@gmail.com",
    description="Bash's textbox package.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bash-elliott/bashbox",
    project_urls={
        "Bug Tracker": "https://github.com/bash-elliott/bashbox/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",

    package_data={'': ["src\\bashbox\\themes\\*.bsh", "init.txt"]},
    include_package_data=True
)
