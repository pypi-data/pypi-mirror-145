import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gfss_microsoft",
    version="0.0.2",
    author="John",
    author_email="john.doe@mail.com",
    description="gfss_microsoft",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.placeholder",
    project_urls={
        "Bug Tracker": "https://www.placeholder",
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
