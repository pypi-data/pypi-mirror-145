import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_desc = f.read()

setuptools.setup(
    name="pymatchlib",
    version="0.1-1",
    author="tpxHorus",
    description="A package for calculating various equations",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/pymatchlib",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.10",
)
