from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='techai',
  version='2.2.2',
  description='can be used to make simple neural networks.',
  long_description=open('README.txt').read(),
  url='',  
  author='Technik',
  author_email='makemyclick3@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='Techai easy AI Tool',
  packages=find_packages(),
  install_requires=['numpy'] 
)
