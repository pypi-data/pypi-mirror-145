from setuptools import find_packages, setup
import os


def get_version():
    HERE = os.path.dirname(__file__)
    with open(os.path.join(HERE, NAME, "__version__.py")) as f:
        return f.read().strip()


NAME = "flask_theme_adminlte3"
VERSION = get_version()

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join("..", path, filename))
    print(f"Package Files: {paths}")
    return paths


REQUIREMENTS = [
    "flask","pyyaml"
]
DEV_REQUIREMENTS = [
    "wheel","twine",
    "pytest", 
    "flask-debugtoolbar",
    "flask-assets",
    "jsmin",
    "cssmin",    
    "pre-commit",
    "flask-mkdocs"
]

setup(
    name=NAME,
    version=VERSION,
    packages=find_packages(exclude=['']),
    package_data={NAME: package_files(NAME)},
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIREMENTS,
    extras_require={
        "dev": DEV_REQUIREMENTS,
    }
)
