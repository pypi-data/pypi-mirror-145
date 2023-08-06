from pathlib import Path

from setuptools import find_packages, setup


HERE = Path(__file__).parent
README = HERE.joinpath("README.md").read_text()
# REQUIREMENTS = HERE.joinpath("requirements", "requirements.in").read_text().split()

REQUIREMENTS = [
    'attrs==21.4.0',
    'certifi==2021.10.8',
    'charset-normalizer==2.0.12',
    'click==8.0.4',
    'flask==2.0.3',
    'flask-classful==0.14.2',
    'idna==3.3',
    'iniconfig==1.1.1',
    'itsdangerous==2.1.1',
    'jinja2==3.0.3',
    'jsonpickle==2.1.0',
    'loguru==0.6.0',
    'markupsafe==2.1.1',
    'p2pnetwork==1.1',
    'packaging==21.3',
    'pluggy==1.0.0',
    'py==1.11.0',
    'pycryptodome==3.14.1',
    'pyparsing==3.0.7',
    'pytest==7.1.1',
    'pytest-asyncio==0.18.2',
    'python-dotenv==0.19.2',
    'requests==2.27.1',
    'tomli==2.0.1',
    'urllib3==1.26.9',
    'waitress==2.1.1',
    'werkzeug==2.0.3'
]

def get_version(rel_path: Path):
    contents = HERE.joinpath(rel_path).read_text().splitlines()

    for line in contents:
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


setup(
    name="beez",
    version=get_version(Path("src", "beez", "version.py")),
    author="Enrico Zanardo",
    author_email="enrico.zanardo101@gmail.com",
    description="A Blockchain for Machine Learnig models and Digital Asset Management",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=REQUIREMENTS,
    python_requires=">=3.10.0",
)