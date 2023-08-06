import setuptools

setuptools.setup(
    name = "mft_math", #should be unique in pypi packages
    version = "1.0.0",
    long_description = open("README.md").read(),
    packages=setuptools.find_packages(exclude=["env"]) #these packages will be excluded
)