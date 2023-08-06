import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

PKG_NAME = "oneneuron_pkg"
PROJECT_NAME = 'Oneneuron_pkg'
USER_NAME = "pk1308"

setuptools.setup(
    name=f"{PKG_NAME}-{USER_NAME}",
    version="0.0.4",
    author=USER_NAME,
    author_email="princevkurien@gmail.com",
    description="A small package for perceptron",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/pk1308/oneneuronpackage",
    project_urls={
        "Bug Tracker": f"https://github.com/pk1308/oneneuronpackage/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        "numpy==1.21.4",
        "pandas==1.3.4",
        "joblib==1.1.0"
    ]
)