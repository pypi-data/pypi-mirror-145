from setuptools import setup, find_packages

from py_sa._version import __version__

setup(name='pysa_aws',
      version=__version__,
      description='Interact with aegea and s3 through python',
      packages=find_packages(),
      author='Matt Olm',
      author_email='mattolm@stanford.edu',
      license='MIT',
      install_requires=[
          'pandas',
          'boto3'
      ],
      zip_safe=False)
