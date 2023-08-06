import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="uselesspackage",
    version="0.0.2",
    author="Nikolai Limbrunner",
    author_email="nikolai.limbrunner@gmail.com",
    description="Useless package for demo purposes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"uselesspackage": "uselesspackage"},
    packages=["uselesspackage"],
    python_requires=">=3.6",
)
