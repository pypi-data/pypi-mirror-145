import setuptools
 
with open("README.md", 'r') as fh:
    long_description = fh.read()
 
setuptools.setup(
    name="float1234",
    version="1.0",
    author="xxx",
    author_email="wanghaoming17@163.com",
    description="一个很NB的包",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="github地址",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[
        "pillow"
    ],
    python_requires=">=3",
)
