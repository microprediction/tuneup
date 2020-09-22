import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="microcorporates",
    version="0.0.1",
    description="Sugar for optuna and use with filtering",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/microprediction/tuneup",
    author="microprediction",
    author_email="pcotton@intechinvestments.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["microcorporates"],
    test_suite='pytest',
    tests_require=['pytest'],
    include_package_data=True,
    install_requires=["pandas","numpy","pytest","python-dateutil","statsmodels","microfilter","optuna", "sklearn","microconventions", "deap"],
    entry_points={
        "console_scripts": [
            "microcorporates=microcorporates.__main__:main",
        ]
    },
)
