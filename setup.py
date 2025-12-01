from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="adipose",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Generate backend and frontend API layers from a single config",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/adipose",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "adipose=adipose.cli.main:cli",
        ],
    },
    include_package_data=True,
    package_data={
        "adipose": [
            "templates/**/*",
        ],
    },
)
