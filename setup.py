import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cropping_package",
    version="0.0.1",
    author="sondrtha",
    description="A small image cropping package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sondrtha/ImageCropping.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows"
    ],
    python_requires='>=3.6',
)

