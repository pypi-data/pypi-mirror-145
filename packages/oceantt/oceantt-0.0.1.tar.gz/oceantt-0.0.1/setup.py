from setuptools import setup, find_packages
import os

ROOT_DIR='oceantt'
with open(os.path.join(ROOT_DIR, 'VERSION')) as version_file:
    version = version_file.read().strip()

setup(name='oceantt',
      version=version,
      description='oceantt: Ocean Microstructure Toolbox',
      long_description='oceantt: Toolbox to process microstructure data from turbulence profilers',
      url='https://github.com/MarineDataTools/oceantt',
      author='oceantt developers',
      author_email='peter.holtermann@io-warnemuende.de',
      license='GPLv03',
      packages=['oceantt'],
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
