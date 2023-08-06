import setuptools

PACKAGE_NAME = 'airflow-gcpsecretmanager-adapter'
PACKAGE_VERSION = '0.0.7'

REQUIRED_PACKAGES = [
    "apache-airflow-backport-providers-google==2021.3.3",
]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name=PACKAGE_NAME,
    version=PACKAGE_VERSION,
    author="Trustpilot",
    author_email="jge@trustpilot.com",
    description='Airflow GCP Secret Manager adapter',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/trustpilot/airflow-gcpsecretmanager-adapter",
    project_urls={
        "Bug Tracker": "https://github.com/trustpilot/airflow-gcpsecretmanager-adapter/issues"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    packages=["airflow_gcpsecretmanager_adapter"],
    python_requires=">=3.6",
    install_requires=REQUIRED_PACKAGES,
)
