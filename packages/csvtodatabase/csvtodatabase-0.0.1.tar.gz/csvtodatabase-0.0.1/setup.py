import setuptools

with open("README.md", "r") as fh:
 long_description = fh.read()

setuptools.setup(
 name='csvtodatabase',
 version='0.0.1',
 author="Haridas",
 author_email="vrharidas141@gmail.com",
 description="This package add the data of csv file to database and allows to perform crud operations on it",
 long_description=long_description,
 long_description_content_type="text/markdown",
 packages=setuptools.find_packages(),
 classifiers=[
 "Programming Language :: Python :: 3",
 "License :: OSI Approved :: MIT License",
 "Operating System :: OS Independent",
 ],
 py_modules=['csvtodatabase'],
 package_dir={'':'src'},
 install_requires=[
  'Jinja2',
  'mysql-connector-python',
  'pandas',
 ]
)