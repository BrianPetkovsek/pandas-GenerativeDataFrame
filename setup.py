from setuptools import setup, find_packages
try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements

install_reqs = parse_requirements("requirements.txt", session=False)
requirements = []
try:
    requirements = [str(ir.req) for ir in install_reqs]
except:
    requirements = [str(ir.requirement) for ir in install_reqs]

setup(
    name='pandas-GenerativeDataFrame',
    version='0.0.1',
    description='pandas-GenerativeDataFrame',
    url='git@github.com:BrianPetkovsek/pandas-GenerativeDataFrame.git',
    author='Brian Petkovsek',
    author_email='',
    license='GNU GENERAL PUBLIC LICENSE',
    packages=find_packages(),
    install_requires=requirements,
    zip_safe=False
)