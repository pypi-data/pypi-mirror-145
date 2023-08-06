import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gfss-outlook-api",
    version="0.0.1",
    author="Damian",
    author_email="piatkowki.damian@quintiles.com",
    description="GFSS outlook api module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlabrnds.quintiles.com/gfss-automation-and-analytics/all/040_elk_logger",
    project_urls={
        "Bug Tracker": "https://gitlabrnds.quintiles.com/gfss-automation-and-analytics/all/040_elk_logger",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)