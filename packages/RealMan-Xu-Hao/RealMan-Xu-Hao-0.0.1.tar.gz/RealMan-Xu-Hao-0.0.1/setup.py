import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="RealMan-Xu-Hao",
    version="0.0.1",
    author="Xu, Hao",
    author_email="xuhao@psyai.net",
    description="An effort to create digital human looks and moves like a real person",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/veryverypro/RealMan",
    project_urls={
        "Bug Tracker": "https://github.com/veryverypro/RealMan/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "real_man"},
    packages=setuptools.find_packages(where="real_man"),
    python_requires=">=3.6",
)