from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

## edit below variables as per your requirements -
REPO_NAME = "Sistem Rekomendasi Buku Berbasis Machine Learning"
AUTHOR_USER_NAME = "SYAIFUL HENDRI IRAWAN"
SRC_REPO = "rekomendasi_buku"
LIST_OF_REQUIREMENTS = []


setup(
    name=SRC_REPO,
    version="0.0.1",
    author="SYAIFUL HENDRI IRAWAN",
    description="Paket kecil lokal untuk rekomendasi buku berbasis ML",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/syaifulhendriirawan/Sistem-Rekomendasi-Buku",
    author_email="syaifulhendriirwn@gmail.com",
    packages=find_packages(),
    license="MIT",
    python_requires=">=3.7",
    install_requires=LIST_OF_REQUIREMENTS
)