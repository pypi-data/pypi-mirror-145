import pathlib
from setuptools import setup


HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="chalice-veneer",
    version="0.0.26",
    description="Class based routing for Chalice with built in validation through Pydantic",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/KristaBliss/chalice-veneer",
    author="Krista Bliss",
    author_email="contact@kristabliss.com",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    py_modules=["chalice_veneer"],
    packages=["chalice_veneer"],
    include_package_data=True,
    install_requires=["pydantic"],
    python_requires=">=3.7",
    zip_safe=False,  # https://mypy.readthedocs.io/en/latest/installed_packages.html
)
