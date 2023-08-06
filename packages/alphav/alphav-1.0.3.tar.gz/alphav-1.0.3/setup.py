import setuptools

setuptools.setup(
    name="alphav",
    author="daniel tal",
    requires=["setuptools"],
    install_requires=["certifi==2021.10.8",
                      "charset-normalizer==2.0.12",
                      "idna==3.3",
                      "numpy==1.22.3",
                      "pandas==1.4.2",
                      "python-dateutil==2.8.2",
                      "pytz==2022.1",
                      "requests==2.27.1",
                      "six==1.16.0",
                      "urllib3==1.26.9"],
    author_email="daniel@dtsoft.co.il",
    description="alpha vantage api wrapper",
    url="https://github.com/dt-ss/alphav",
    python_requires='>=3.7',
    version="1.0.3",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
