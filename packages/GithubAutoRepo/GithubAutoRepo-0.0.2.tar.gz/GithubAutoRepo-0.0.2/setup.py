from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='GithubAutoRepo',
  version='0.0.2',
  description='Github Auto Repo Creator',
  long_description=open('CHANGELOG.txt').read(),
  url='',  
  author='Subham Rouniyar',
  author_email='subham.rouniyar27@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='githubrepository', 
  packages=find_packages(),
  install_requires=['requests'] 
)