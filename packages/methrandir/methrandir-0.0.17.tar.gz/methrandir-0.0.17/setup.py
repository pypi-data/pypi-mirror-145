import setuptools
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="methrandir",
    version=os.environ.get("CI_COMMIT_TAG"),
    author="Skander Hatira",
    author_email="skander.hatira@inrae.fr",
    description="Python utility for understanding whole genome bisulfite data and viewing it as a whole",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://forgemia.inra.fr/skander.hatira/methrandir",
    project_urls={
        "Bug Tracker": "https://forgemia.inra.fr/skander.hatira/methrandir/-/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8.5",
    entry_points={
    'console_scripts': [
        'methrandir = methrandir:methrandir.main',
    ],
},
    install_requires=[
        "scikit-learn",
        "pandas",
        "plotly",
        "kaleido"
    ],
)