from setuptools import find_packages, setup

setup(
    name="mcqgenerator",
    version="0.0.1",
    author="Nadir Askarov",
    author_email="nadirr2609@gmail.com",
    install_requires=[
        "openai",
        "langchain",
        "langchain-openai",
        "langchain-community",
        "streamlit",
        "python-dotenv",
        "PyPDF2",
        "pandas",
    ],
    packages=find_packages(),
)
