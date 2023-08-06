from setuptools import (
    find_packages,
    setup,
)

setup(
    name="fluid-setup",
    version="0.0.1",
    license="MIT",
    author="Andres Galvan",
    author_email="andresgalfajar@gmail.com",
    packages=find_packages("./"),
    package_dir={"": "./"},
    url="https://github.com/afgalvan/fluid-setup",
    keywords="fluidattacks setup",
    install_requires=["pyyaml", "loguru"],
)
