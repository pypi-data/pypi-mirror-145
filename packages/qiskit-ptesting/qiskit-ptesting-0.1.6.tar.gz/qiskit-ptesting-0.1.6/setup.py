from setuptools import setup, find_packages
import os
from setuptools import setup

README_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md')
with open(README_PATH) as readme_file:
        README = readme_file.read()

setup(
    name="qiskit-ptesting",
    version="0.1.6",
    description="Property-based testing framework for qiskit algorithms.",
    long_description=README,
    long_description_content_type='text/markdown',
    license="Apache 2.0",
    author="Pierre Brassart",
    author_email="pierrebrassart80@hotmail.fr",
    packages=find_packages("src"),
    package_dir={"": "src"},
    url="https://gitlab.com/twistercool/Qiskit-PTesting",
    classifiers=[
        "Development Status :: 3 - Alpha",
        ],
    keywords="qiskit property testing",
    install_requires=[
            "qiskit",
            "scipy",
            "numpy"
        ],
    python_requires=">=3.6",
)
