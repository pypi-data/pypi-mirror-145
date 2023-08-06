from setuptools import setup, find_packages

with open('README.md', encoding="utf-8") as f:
    readme = f.read()

with open('LICENSE', encoding="utf-8") as f:
    license = f.read()

setup(
    name='bodotokenizer',
    version='0.1.0',
    description='Package for Bodo Tokenizer',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='Maharaj Brahma',
    author_email='mraj.brahma@gmail.com',
    url='https://github.com/bodonlp/bodo-tokenizer',
    license=license,
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    python_requires=">=3.6",
    keywords=['Bodo language', 'Bodo Tokenizer'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)