from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='webthon',
  version='0.0.1',
  description='This is simple html generator for flask or django',
  long_description=open('README.rst').read(),
  url='',  
  author='mario1842',
  author_email='mario1842.info@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='flask html css generator django',
  packages=find_packages(),
  install_requires=[] 
)
