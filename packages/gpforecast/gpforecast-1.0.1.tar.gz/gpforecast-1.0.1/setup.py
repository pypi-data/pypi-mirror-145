import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name="gpforecast", 
     version='1.0.1',
     description="Time series forecasting with Gaussian Processes",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/IDSIA/gpforecasting",
     author="Huber David, Rubattu Nicolo', Corani Giorgio",
     author_email="david.huber@idsia.ch, nicolo.rubattu@idsia.ch, giorgio.corani@idsia.ch",
     license="BSD License",
     classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.8",
     ],
     packages=['gpforecast', 'tutorial'],
     include_package_data=True,
     install_requires=["numpy", "pandas", "scipy", "GPy", "properscoring", "matplotlib", "packaging"],
 )