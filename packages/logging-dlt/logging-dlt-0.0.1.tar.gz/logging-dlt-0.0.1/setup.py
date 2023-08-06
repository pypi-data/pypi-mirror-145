import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="logging-dlt",
    version="0.0.1",
    author="Patrick Menschel",
    author_email="menschel.p@posteo.de",
    description="A python logging adapter for diagnostic log and trace protocol.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/menschel/logging-dlt",
    packages=setuptools.find_packages(exclude=["tests", "scripts", ]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: POSIX :: Linux",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Embedded Systems",
    ],
    python_requires=">=3.9",
    keywords="logging",
    requires=["pyserial", ],
)
