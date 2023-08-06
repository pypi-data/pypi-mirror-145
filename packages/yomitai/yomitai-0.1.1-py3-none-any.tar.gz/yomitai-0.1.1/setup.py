from setuptools import setup, find_packages
from yomitai import __version__

setup(name='yomitai',
      version=__version__,
      url='https://github.com/noxowl/yomitai',
      license='MIT',
      author='Suyeong RHIE',
      author_email='me@euc-kr.net',
      description='CLI Application for quick reference of Japanese-Yomikata',
      packages=find_packages(exclude=['tests']),
      long_description=open('README.md').read(),
      zip_safe=False,
      classifiers=[
          "Programming Language :: Python :: 3.9",
          "License :: OSI Approved :: MIT License",
          "Development Status :: 3 - Alpha",
          "Intended Audience :: Education",
          "Natural Language :: Japanese"
      ],
      install_requires=['typer>=0.4.0', 'pykakasi>=2.2.1'],
      python_requires='>=3.9')
