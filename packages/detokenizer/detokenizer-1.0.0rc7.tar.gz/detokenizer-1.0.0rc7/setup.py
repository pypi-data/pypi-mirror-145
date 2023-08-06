
import re
from setuptools import setup


version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('detokenizer/__init__.py').read(),
    re.M
    ).group(1)


with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")


setup(
    name = "detokenizer",
    packages = ["detokenizer"],
    entry_points = {
        "console_scripts": ['detokenizer = detokenizer.__main__:main']
        },
    version = version,
    description = "Python command line for property injection.",
    long_description = long_descr,
    long_description_content_type='text/markdown',
    author = "Matthias Müller",
    author_email = "matthias.mueller@salt.ch",
    url = "https://gitlab-it.salt.ch/tools/detokenizer",
    install_requires=[
        'pyyaml'
        ]
    )
