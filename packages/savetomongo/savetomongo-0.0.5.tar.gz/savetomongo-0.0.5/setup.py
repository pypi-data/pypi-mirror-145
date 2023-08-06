import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="savetomongo",
  version="0.0.5",
  author="zhaoyun",
  author_email="1246192877@qq.com",
  description="This is a module for importing dictionary or list data into mongodb database. Before importing, it will check for duplication. If it exists, it will not be imported. If it does not exist, it will be imported. The standard for checking whether there is duplication is a relatively unique key.",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)