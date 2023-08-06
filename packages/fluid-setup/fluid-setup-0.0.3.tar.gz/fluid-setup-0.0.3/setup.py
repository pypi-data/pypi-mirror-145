from importlib.metadata import (
    entry_points,
)
from setuptools import (
    find_packages,
    setup,
)

setup(
    name="fluid-setup",
    version="0.0.3",
    license="MIT",
    author="Andres Galvan",
    author_email="andresgalfajar@gmail.com",
    packages=find_packages("src"),
    package_dir={"": "src"},
    url="https://github.com/afgalvan/fluid-setup",
    keywords="fluidattacks setup",
    install_requires=["pyyaml", "loguru"],
    entry_points={"console_scripts": ["fluid-setup=fluid:main"]},
)
