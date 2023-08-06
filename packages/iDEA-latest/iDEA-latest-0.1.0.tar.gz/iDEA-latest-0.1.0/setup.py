import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="iDEA-latest",
    version="0.1.0",
    author="Jack Wetherell",
    author_email="jack.wetherell@gmail.com",
    description="interacting Dynamic Electrons Approach (iDEA)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iDEA-org/iDEA",
    project_urls={
        "Bug Tracker": "https://github.com/iDEA-org/iDEA/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
)