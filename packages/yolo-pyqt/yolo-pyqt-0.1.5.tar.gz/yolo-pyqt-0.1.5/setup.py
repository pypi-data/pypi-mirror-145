import os
from setuptools import setup, find_packages


def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


setup(
    name="yolo-pyqt",
    version="0.1.5",
    author="Tao Yang",
    author_email="ytaofighting@gmail.com",
    description="yolo-pyqt provides an easy way to build automated quantitative trading systems for individual traders.",
    license="Apache License 2.0",
    keywords="quantitative-trading qt api",
    url="https://github.com/TaoYang526/yolo-pyqt",
    packages=['pyqt', 'pyqt.api', 'pyqt.api.impl', 'pyqt.utils'],
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Utilities",
        'License :: OSI Approved :: Apache Software License',
        "Programming Language :: Python :: 3"
    ],
)
