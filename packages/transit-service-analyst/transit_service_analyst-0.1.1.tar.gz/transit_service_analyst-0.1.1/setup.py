from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.readlines()

setup (
    name="transit_service_analyst",
    version = "0.1.1",
    author="psrc staff",
    author_email="scoe@psrc.org",
    description = "Tools to support transit service analysis",
    python_requires=">=3.8",
    keywords ='GTFS',
    install_requires = requirements,
    license ='MIT',
    packages = find_packages(),
)