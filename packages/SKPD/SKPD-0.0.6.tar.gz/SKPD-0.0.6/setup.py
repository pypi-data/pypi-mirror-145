import os
from setuptools import setup, find_packages


path = os.path.abspath(os.path.dirname(__file__))

try:
  with open(os.path.join(path, 'README.md')) as f:
    long_description = f.read()
except Exception as e:
  long_description = "SKPD: A General Framework of Signal Region Detection in Image Regression"

setup(
    name = "SKPD",
    version = "0.0.6",
    # keywords = ("pip", "SKPD", "image-regression"),
    description = "image regression",
    long_description = long_description,
    long_description_content_type='text/markdown',
    python_requires=">=3.7.0",
    license = "MIT Licence",

    url = "https://github.com/SanyouWu/SKPD",
    author = "Sanyou WU",
    author_email = "sanyouwsy@gmail.com",

    # packages = find_packages(),
    packages = ["SKPD"],
    include_package_data = True,
    install_requires = ["scikit-learn","joblib","matplotlib"], # sklearn, numpy, pandas
    platforms = "all",

    scripts = [],
    # entry_points = {
    #     'console_scripts': [
    #         'skpdRegressor:'
    #     ]
    # }
)
