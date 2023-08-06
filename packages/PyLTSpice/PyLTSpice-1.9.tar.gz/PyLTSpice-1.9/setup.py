import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='PyLTSpice',
    version='1.9',
    scripts=['PyLTSpice/__init__.py',
             'PyLTSpice/Histogram.py',
             'PyLTSpice/LTSpice_RawRead.py',
             'PyLTSpice/LTSpice_RawWrite.py',
             'PyLTSpice/LTSpiceBatch.py',
             'PyLTSpice/LTSteps.py',
             'PyLTSpice/LTSpice_SemiDevOpReader.py',
             # 'PyLTSpice/sketch.py'
             ],
    # install_requires = [],
    author="Nuno Brum",
    author_email="me@nunobrum.com",
    description="An set of tools to Automate LTSpice simulations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nunobrum/PyLTSpice",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
