import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qwizkoolnlp",
    version="0.0.1",
    author="kgvinod",
    author_email="kgvinod@gmail.com",
    description="Qwizkool NLP based library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kgvinod/qwizkoolnlp",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Propreitary License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    test_suite="tests",
)
