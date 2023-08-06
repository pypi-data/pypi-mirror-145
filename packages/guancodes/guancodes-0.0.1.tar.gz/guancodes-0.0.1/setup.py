from setuptools import setup

setup(
    name='guancodes',
    version='0.0.1',
    packages=['guancodes'],
    install_requires=[
        'requests',
        'importlib-metadata; python_version == "3.8"',
    ],
)