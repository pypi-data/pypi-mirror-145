import os
import io
import setuptools

with open("README.md", "r", encoding='UTF-8') as fh:
    long_description = fh.read()

if os.path.exists("requirements.txt"):
    install_requires = io.open("requirements.txt").read().split("\n")
else:
    install_requires = []

setuptools.setup(
    name="msinfo",  # Replace with your own username
    version="0.0.1",
    author="xunull",
    author_email="xunull@163.com",
    description="show model info",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xunull/msinfo",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)
