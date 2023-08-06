import setuptools

with open("README.md", "r") as fhandle:
    long_description = fhandle.read() # Your README.md file will be used as the long description!

setuptools.setup(
    name="swear", # Put your username here!
    version="3.14159", # The version of your package!
    author="someStranger8", # Your name here!
    author_email="someStranger87@gmail.com", # Your e-mail here!
    description="A module that displays cool ascii banners of curse words", # A short description here!
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/someStranger8/swear", # Link your package website here! (most commonly a GitHub repo)
    packages=setuptools.find_packages(), # A list of all packages for Python to distribute!
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ], # Enter meta data into the classifiers list!
    python_requires='>=3.6', # The version requirement for Python to run your package!
)
