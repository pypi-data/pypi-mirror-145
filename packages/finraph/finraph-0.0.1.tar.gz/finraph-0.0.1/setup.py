from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='finraph',
  version='0.0.1',
  description='Graph analysis on Traded Companies',
  long_description=open('README').read() + '\n\n' + open('CHANGELOG').read(),
  url='',  
  author='ROhit Gupta',
  author_email='gupta.rohit21198@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='finance graphs', 
  packages=find_packages(),
  install_requires=[''] 
)