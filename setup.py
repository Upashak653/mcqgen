from setuptools import find_packages,setup

setup(
    name="mcqgenerator",
    version="0.0.1",
    author="upashak",
    author_email="upashak1817@gmail.com",
    install_requires=["openai","langchain","PyPDF2","python-dotenv","streamlit"],
    packages=find_packages()
)