import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-pt-at-qr-code",
    version="0.0.1",
    author="Bruno Tavares",
    author_email="tavares.b@gmail.com",
    description="Portuguese fiscal documents QR Code library",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/tavaresb/python-pt-at-qr-code",
    project_urls={
        "Bug Tracker": "https://github.com/tavaresb/python-pt-at-qr-code/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    test_suite='nose.collector',
    tests_require=['nose'],
)
