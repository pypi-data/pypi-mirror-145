from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='micode.py',
  version='1.0.0',
  description='Moja biblioteka (Miki3oo5)',
  long_description=open('README.rst').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Miki3oo5',
  author_email='mikolajzelazny5@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='Miki3oo5',
  packages=find_packages(),
  install_requires=['Pillow','easy-pil', 'discord.py'] 
)