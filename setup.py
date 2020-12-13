from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

__author__ = "Denis Mulyalin <d.mulyalin@gmail.com>"

setup(
    name="ttp_templates",
    version="0.1.0",
    author="Denis Mulyalin",
    author_email="d.mulyalin@gmail.com",
    description="Template Text Parser Templates collections",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dmulyalin/ttp_templates",
    packages=setuptools.find_packages(),
    extras_require={},
    include_package_data=True,
    package_data={
        "ttp_templates": [
            "platform/*.txt", 
            "yang/*.txt",
            "misc/*/*.txt"
            ]
    },
    data_files=[('', ['LICENSE'])],
    classifiers=[
        "Topic :: Utilities",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
