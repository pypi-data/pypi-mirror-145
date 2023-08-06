import setuptools
 
with open("README.md", 'r') as fh:
    long_description = fh.read()
 
setuptools.setup(
    name="fineng_model",
    version="0.1",
    author="haoming wang",
    author_email="wanghaoming17@163.com",
    description="financial model",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="github地址",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ],
    install_requires=[
        "numpy"
    ],
    python_requires=">=3",
)
