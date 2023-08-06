import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="korea-public-data",  # Replace with your own PyPI username(id)
    version="0.0.1",
    author="JAY",
    author_email="root@ja-y.com",
    description="Korea Public Data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ja-y-com/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
