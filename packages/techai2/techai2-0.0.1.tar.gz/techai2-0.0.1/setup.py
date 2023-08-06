from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='techai2',
  version='0.0.1',
  description='Neural Network Tool For Advanced And Big Neural Networks',
  long_description=open('README.txt').read(),
  url='',  
  author='Technik',
  author_email='makemyclick3@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='techai2 NeuralNetworks AI tool',
  packages=find_packages(),
  install_requires=['numpy'] 
)
