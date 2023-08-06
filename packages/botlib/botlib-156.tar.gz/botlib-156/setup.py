# This file is placed in the Public Domain.


from setuptools import setup


def read():
    return open("README.rst", "r").read()


setup(
    name="botlib",
    version="156",
    url="https://github.com/bthate/botlib",
    author="Bart Thate",
    author_email="bthate67@gmail.com",
    description="the python3 bot namespace.",
    long_description=read(),
    install_requires=["libobj"],
    packages=["bot"],
    namespace_packages=["bot"],
    license="Public Domain",
    scripts=["bin/bot"],
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: Public Domain",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Topic :: Utilities",
    ],
)
