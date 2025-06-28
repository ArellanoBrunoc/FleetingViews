from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="fleetingviews",
    version="0.2.dev5066",
    author="Bruno Arellano",
    author_email="arellanobruno@hotmail.com",
    py_modules=['FleetingViews'],
    license="MIT",
    maintainer="Bruno Arellano",
    maintainer_email="arellanobruno@hotmail.com",
    keywords=["flet", "views", "flet views", "view creation", "flet app"],
    description="Facilitates view creation and management in Flet applications.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ArellanoBrunoc/FleetingViews",
    include_package_data=True,
    install_requires=[
        "flet"
    ],
)
