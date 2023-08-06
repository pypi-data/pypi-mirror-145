import pathlib

from setuptools import setup

install_requires = [
    "zeep~=4.1.0",
    "pytz==2022.1",
]

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="Global Processing Services Client",
    version="0.0.1",
    description="Client library for Global Processing Services",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Hammy Goonan",
    author_email="hammy@divipay.com",
    url="https://github.com/divipayhq/py-gps-client",
    python_requires=">=3.8",
    install_requires=install_requires,
    license="MIT",
    package_dir={"": "src"},
    packages=["globalprocessing_client"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
)
