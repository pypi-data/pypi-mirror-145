from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="databeaver",
    version="0.0.2",
    author="David Orkin",
    author_email="david.orkin@fuzzybumblebee.org",
    description="Data Beaver - Data Modelling Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://opensource.fuzzybumblebee.org/databeaver",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    data_files=[('sample-project', ['databeaver.toml'])],
    install_requires=['tomli'],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
    scripts=['bin/beaver']
)



