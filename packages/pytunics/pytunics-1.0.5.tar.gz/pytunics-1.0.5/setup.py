import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytunics",
    version="1.0.5",
    author="Kostiantyn Vasko",
    author_email="kostiantyn.vasko@nure.ua",
    description="package with main method for laser control",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.xlim.fr/vasko/Tunics-Laser-control-python",
    project_urls={
        "Bug Tracker": "https://gitlab.xlim.fr/vasko/Tunics-Laser-control-python/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
)