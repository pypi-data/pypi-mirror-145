"""
https://packaging-python.org/tutorials/packaging-projects/


"""

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="latestearthquake-indonesia.1",
    version="0.5",
    author="Wildan Aruman",
    author_email="wildan.aruman90@gmail.com",
    description="This package will get the latest earthquake from BMKG | Indonesian Agency for Meteorological, Climatological and Geophysics ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/WildanAruman/deteksi-gempa-terkini",
    project_urls={
        "Bug Tracker": "https://github.com/WildanAruman/deteksi-gempa-terkini",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable"
    ],
  #  package_dir={"": "src"},
  #  packages=setuptools.find_packages(where="src"),
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
