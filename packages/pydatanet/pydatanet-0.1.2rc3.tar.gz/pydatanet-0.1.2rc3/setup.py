
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pydatanet",
    version="0.1.2rc3",
    author="xTrayambak",
    author_email="xtrayambak@gmail.com",
    description="A fancy networking library which supports both the protocols and makes it hard to shoot yourself in the foot.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xTrayambak/pysyn",
    project_urls={
        "Bug Tracker": "https://github.com/xTrayambak/pysyn/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src/"},
    packages=setuptools.find_packages(where="src/"),
    python_requires=">=3.8",
)
