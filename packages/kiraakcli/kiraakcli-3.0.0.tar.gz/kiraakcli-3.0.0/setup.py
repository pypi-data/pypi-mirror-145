import pathlib

from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="kiraakcli",
    version="3.0.0",
    description="Add orders to the Kiraak API",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Vthechamp22",
    author="Vthechamp",
    author_email="parashar.xtra@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["kiraak"],
    include_package_data=True,
    install_requires=["requests", "click", "openpyxl", "colorama", "rich", "woocommerce"],
    entry_points={
        "console_scripts": [
            "kcli=kiraak.__main__:kcli.cli",
        ]
    },
)
