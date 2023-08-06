import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="smilecoin",
    version="1.0.14",
    author="Nick Bucheleres",
    author_email="nick@smilecoin.us",
    description="Smile Coin Python SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SmileCoinUS/smilecoin-sdk",
    project_urls={
        "Bug Tracker": "https://github.com/SmileCoinUS/smilecoin-sdk",
        "Documentation": "https://smile-coin.gitbook.io/sdk-docs/"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    # packages=setuptools.find_packages(include=['smilecoin', 'smilecoin-sdk', 'smilecoin-sdk.*']),
    packages=['smilecoin'],
    install_requires=['requests', 'json'],
    python_requires=">=3.6",
)