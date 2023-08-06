from setuptools import setup, find_packages
import os

ROOT_DIR='oceanmic'
with open(os.path.join(ROOT_DIR, 'VERSION')) as version_file:
    version = version_file.read().strip()

setup(name='oceanmic',
      version=version,
      description='oceanmic: Ocean Microstructure Toolbox',
      long_description='oceanmic: Toolbox to process microstructure data from turbulence profilers',
      url='https://github.com/MarineDataTools/oceanmic',
      author='oceanmic developers',
      author_email='peter.holtermann@io-warnemuende.de',
      license='GPLv03',
      packages=['oceanmic'],
      #packages=find_packages(),
      scripts = [],
      entry_points={ 'console_scripts': []},
      package_data = {'':['VERSION']},
      install_requires=[],
      classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Scientific/Engineering',          
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',  
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
      ],
      python_requires='>=3.5',
      zip_safe=False)
