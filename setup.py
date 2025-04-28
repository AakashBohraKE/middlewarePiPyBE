from setuptools import setup, find_packages

setup(
    name="fastapi_error_logger",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.109.2",
        "starlette>=0.36.3",
    ],
    author="Aakash Bohra",
    author_email="aakash.bohra@knowledgeexcel.com",
    description="A FastAPI middleware for comprehensive error logging",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/AakashBohraKE/middlewarePiPyBE",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
) 