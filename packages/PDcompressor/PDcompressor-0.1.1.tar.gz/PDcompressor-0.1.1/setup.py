import setuptools

setuptools.setup(
    name="PDcompressor", # Replace with your own username
    version="0.1.1",
    author="papamoon0113",
    author_email="papamoon0113@pusan.ac.kr",
    description="Package for compress storage dataframe",
    long_description="",
    long_description_content_type="text/markdown",
    url="https://github.com/Ho-Jun-Moon/pandas_storage_compressor",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires = ['pandas', 'numpy'],
)   