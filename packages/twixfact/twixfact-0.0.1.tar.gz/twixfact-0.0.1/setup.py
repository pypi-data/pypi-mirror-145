from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Factorial Package'
LONG_DESCRIPTION = 'You can calculate factorial using this package'

# Setting up
setup(
    name="twixfact",
    version=VERSION,
    author="twixour (Raushan Kashyap)",
    author_email="<twixour@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'factorial'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
