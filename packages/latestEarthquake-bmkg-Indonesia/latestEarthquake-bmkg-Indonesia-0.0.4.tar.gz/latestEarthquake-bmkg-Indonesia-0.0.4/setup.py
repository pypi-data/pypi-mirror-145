# https://packaging.python.org/en/latest/tutorials/packaging-projects/
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="latestEarthquake-bmkg-Indonesia",
    version="0.0.4",
    author="TheoBrata",
    author_email="theodoresibp@gmail.com",
    description="This package will get the latest earthquake in Indonesia from BMKG | Meteorological, Climatological, "
                "and Geophysical Agency",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/theodoresibp/latest-indonesia-earthquake",
    project_urls={
        "Website": "https://github.com/theodoresibp/latest-indonesia-earthquake",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
    ],
    # package_dir={"": "src"},
    # packages=setuptools.find_packages(where="src"),
    packages=setuptools.find_packages(),
    python_requires=">=3.6",

)



