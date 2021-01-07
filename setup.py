import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="tuneup",
    version="0.0.8",
    description="Global optimizer comparison and combination",
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
    packages=["tuneup"],
    test_suite='pytest',
    tests_require=['pytest'],
    include_package_data=True,
    install_requires=["pandas","numpy","pytest","python-dateutil","statsmodels","microfilter",
                      "optuna", "sklearn","scipy","microconventions", "deap","wheel","hyperopt",
                      "statsmodels","ax-platform","pysot","poap","microprediction","Platypus-Opt","sigopt","wheel",
                      "pymoo"],
    entry_points={
        "console_scripts": [
            "tuneup=tuneup.__main__:main",
        ]
    },
)
