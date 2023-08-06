import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='fyers-logger',  
     version='0.1.4',
     author="Fyers-Tech",
     author_email="support@fyers.in",
     description="Fyers Internal Logging Library",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/FyersDev/fyers-logger",
     py_modules=["fyers_logger"],
     install_requires=[
                'aws-lambda-powertools==1.25.5',
          ],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )