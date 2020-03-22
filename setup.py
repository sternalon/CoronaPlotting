from setuptools import setup, find_packages

requires = [
    "pandas",
    "xlrd",
    "matplotlib"
]

dev_require = [
]

setup(
    name="corona-plotting",
    version="1.0.0",
    description="Plot Corona Virus",
    classifiers=["Programming Language :: Python",],
    author="Alon Stern",
    author_email="sternalon@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={"dev": dev_require},
    install_requires=requires,
)
