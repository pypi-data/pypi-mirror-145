from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='HandWrittenDigitRecognition',
  version='0.0.1',
  description='A Handwritten Digit Recognition Neural Network Model: By Pranav Sai',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Pranav Sai',
  author_email='pranavs31899@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='Handwritten Digit Recognition, Neural Networks', 
  packages=find_packages(),
  install_requires=['matplotlib','tensorflow','opencv-python'] 
)