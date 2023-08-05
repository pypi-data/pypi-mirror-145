from setuptools import setup
from setuptools_rust import Binding, RustExtension

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="nors",
    version="0.1.0",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Rust",
        "Operating System :: POSIX",
        "Operating System :: MacOS :: MacOS X",
    ],
    packages=["nors"],
    rust_extensions=[RustExtension(
        "nors.nors", "Cargo.toml", debug=False, binding=Binding.PyO3)],
    include_package_data=True,
    zip_safe=False,
    url="https://github.com/booink/nors/tree/main/bindings/python3",
    description='nors is a Rust program for counting the number of rows and records in a CSV file.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Booink',
    author_email='booink.work@gmail.com',
    keywords=["csv", "counter", "wc"],
)
