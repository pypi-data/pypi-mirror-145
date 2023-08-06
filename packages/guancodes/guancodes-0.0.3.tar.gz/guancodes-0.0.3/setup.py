from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='guancodes',
    version='0.0.3',
    author="Tomasz Rybotycki",
    author_email="rybotycki.tomasz+guancodes@gmail.com",
    long_description=long_description,
    long_description_content_type='text/markdown',
    description="Package for generating Guan Codes",
    packages=['guancodes'],
    install_requires=[
        'requests',
        'importlib-metadata; python_version == "3.8"',
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
    ],
    license="Apache License 2.0.",
)
