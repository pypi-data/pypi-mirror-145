import os
import setuptools

dir_name = os.path.abspath(os.path.dirname(__file__))

version_contents = {}
with open(os.path.join(dir_name, "src", "xbench", "version.py"), encoding="utf-8") as f:
    exec(f.read(), version_contents)

with open(os.path.join(dir_name, "README.md"), "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="xbench",
    version=version_contents["VERSION"],
    author="Impira Engineering",
    author_email="engineering@impira.com",
    description="Document Extraction Benchmark (xbench)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/impira/extraction-benchmark",
    project_urls={
        "Bug Tracker": "https://github.com/impira/extraction-benchmark/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    package_data={"": ["docs/templates/**"]},
    packages=setuptools.find_packages(where="src"),
    entry_points={
        "console_scripts": ["xbench = xbench.cmd.__main__:main"],
    },
    python_requires=">=3.8",
    install_requires=[
        "pydantic",
        "typing",
        "typing_extensions",
        "faker==8.13.2",  # Pin to a specific version for reproducibility
        "openpyxl",
        "Pillow >= 8",
        "pdf2image",
        "numpy",
        "impira == 0.1.7",
        "boto3",
        "textract-trp",
        "requests",
        "myst-parser >= 0.15",
        "sphinx >= 4.3",
    ],
)
