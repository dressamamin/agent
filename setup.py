from setuptools import setup, find_packages

setup(
    name="academic-writing-agent",
    version="1.0.0",
    description="An agent that helps with academic writing and research papers",
    packages=find_packages(),
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "academic-agent=main:main",
        ],
    },
)
