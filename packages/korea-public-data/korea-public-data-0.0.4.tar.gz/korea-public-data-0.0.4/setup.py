import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="korea-public-data",  # Replace with your own PyPI username(id)
    version="0.0.4",
    author="JAY",
    author_email="root@ja-y.com",
    description="Korea Public Data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ja-y-com/korea-public-data/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        "certifi==2021.10.8",
        "charset-normalizer==2.0.12",
        "hangul-utils==0.2",
        "idna==3.3",
        "pytz==2022.1",
        "requests==2.27.1",
        "urllib3==1.26.9",
        "xmltodict==0.12.0"
    ]
)
