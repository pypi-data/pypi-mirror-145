from setuptools import setup, find_packages
from lorettOrbital.orbital import __version__


with open("requirements.txt", 'r') as file:
      requirements =  file.readlines()
 
with open("README.md", "r") as fh:
	long_description = fh.read()

setup(name='lorettOrbital',
      version=__version__,
      url='https://gitlab.com/lpmrfentazis/lorettorbital',
      license='MIT',
      author='MrFentazis',
      author_email='lpmrfentazis@mail.ru',
      description='A module that makes it easier to interact with LORETT hardware and software complexes.',
      long_description=long_description,
      packages=find_packages(),
      install_requires=requirements,
      classifiers=[
		"Programming Language :: Python :: 3.7",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
      python_requires='>=3.7'
      )