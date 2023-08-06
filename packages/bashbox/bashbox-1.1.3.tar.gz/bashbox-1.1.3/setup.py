import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bashbox",
    version="1.1.3",
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
    packages=['bashbox'],
    package_dir={"bashbox": "src/bashbox"},
    package_data={'bashbox': ['themes/*']},
    python_requires=">=3.6",

    include_package_data=True
)
