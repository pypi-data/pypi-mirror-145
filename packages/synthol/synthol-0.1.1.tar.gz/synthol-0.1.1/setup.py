from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="synthol",
    version="0.1.1",
    description="Simple Python3 dependency injector",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Red Balloon Security",
    url="https://gitlab.com/redballoonsecurity/synthol",
    packages=[
        "synthol",
    ],
    ext_modules=[],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Topic :: Software Development",
    ],
    license_files=["LICENSE"],
    install_requires=[
        "typing_inspect~=0.7.1",
    ],
    extras_require={
        "test": [
            "mypy==0.942",
            "pytest~=7.1.1",
            "pytest-asyncio~=0.18.3",
            "pytest-cov~=3.0.0",
        ],
    },
    python_requires=">=3.7",
    project_urls={
        "Bug Tracker": "https://gitlab.com/redballoonsecurity/synthol/-/issues",
    },
)
