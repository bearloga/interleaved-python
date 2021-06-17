from setuptools import (
    setup,
    find_packages
)

from interleaved import __version__ as package_version

setup(
    name="interleaved",
    version=package_version,
    description="Tools for analyzed interleaved search A/B tests",
    install_requires=[
        "numpy>=1.0",
        "scikit-learn>=0.20.0",
        "pandas>=1.0"
    ],
    packages=find_packages(),
    python_requires=">=3.6",
    url="https://github.com/bearloga/interleaved-py",
    author="Wikimedia Foundation Product Analytics team",
    author_email="product-analytics@wikimedia.org",
    license="BSD 3-Clause",
    include_package_data=True,
    package_data={'': ['data/*.csv']},
    tests_require=['pytest']
)
