import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Rnd-str",
    version="0.0.1",
    author="SudoSaeed",
    author_email="DrSudoSaeed@gmail.com",
    description="Random string production library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DrSudoSaeed",
    project_urls={
        "Bug Tracker": "https://github.com/DrSudoSaeed/",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)