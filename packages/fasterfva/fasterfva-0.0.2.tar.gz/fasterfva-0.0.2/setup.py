from setuptools import setup, find_packages

__version__ = "0.0.2"

short_desc = (
    "Faster Flux Variability Analysis - Solve FVA Problems FAST"
)

with open('README.md') as f:
    long_description = f.read()

setup(
    name='fasterfva',
    version=__version__,
    author='Dustin R. Kenefake',
    author_email='Dustin.Kenefake@tamu.edu',
    description=short_desc,
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    url='https://github.com/DKenefake/fasterfva',
    extras_require={},
    install_requires=["numpy",
                      "gurobipy"],
    packages=find_packages(where='src'),
    package_dir={'': 'src'}
)
