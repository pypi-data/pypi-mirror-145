import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mypasswd",
    version="0.0.2",
    author="liuyaping",
    author_email="applesline@163.com",
    description="A simple secure programmer - specific password management tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/applesline/mypasswd",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)