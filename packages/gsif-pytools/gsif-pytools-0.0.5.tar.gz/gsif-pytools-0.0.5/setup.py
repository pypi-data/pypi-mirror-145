from setuptools import setup, find_packages

with open("README.md","r") as readme_file:
   readme = readme_file.read()

requirements = ["pandas","numpy","requests>=2","openpyxl>=3","pytesseract>=0.3.9","opencv-python>=4","pdf2image>=1"]

setup(
   name="gsif-pytools",
   version="0.0.5",
   author="Mingyin Zhu",
   author_email="mzhu0114@gmail.com",
   description="A package with tools to aid Gator Student Investment Fund Portfolio Attribution Specialists.",
   long_description=readme,
   long_description_content_type="text/markdown",
   url="https://github.com/gsifpytools/homepage/",
   packages=find_packages(),
   install_requires=requirements,
   classifiers=[
      "Programming Language :: Python :: 3.10",
      "License :: OSI Approved :: MIT License",

   ],
)


