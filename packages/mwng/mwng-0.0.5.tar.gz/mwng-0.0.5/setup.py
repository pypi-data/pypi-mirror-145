import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mwng",
    version="0.0.5",
    author="Emojipypi",
    author_email="yiufamily.hh@gmail.com",
    description="MediaWiki API for Python 3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Emojigit/mw",
    project_urls={
        "Bug Tracker": "https://github.com/Emojigit/mw/issues",
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Other Audience",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Wiki",
    ],
    # package_dir={"mwng": "mwng"},
    packages=["mwng"],
    python_requires=">=3.6",
    install_requires=["requests","validators"]
)
