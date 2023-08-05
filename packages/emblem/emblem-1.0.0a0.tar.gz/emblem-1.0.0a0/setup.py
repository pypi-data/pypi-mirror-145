import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="emblem",
    version="1.0.0.a0",
    author="Antonio Lopez Rivera",
    author_email="antonlopezr99@gmail.com",
    description="shields.io + colormaps",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alopezrivera/emblem",
    entry_points={
        "console_scripts": [
            "emblem = emblem.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    install_requires=[
        "matplotlib>=3.3.4",
        "requests>=2.27.1"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
