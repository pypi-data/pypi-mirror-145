import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="StdCTL",
    version="0.1.3",
    author="PureOPENS 2022[4]",
    author_email="3597974497@qq.com",
    description="prompt for stdin/out",
    long_description=long_description,
    url="https://github.com/xkcb1/prompt.git",
    project_urls={
        "Bug Tracker": "https://github.com/xkcb1/prompt.git",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)