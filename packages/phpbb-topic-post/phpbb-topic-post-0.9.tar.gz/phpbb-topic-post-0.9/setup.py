from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.MD'), encoding='utf-8') as f:
    long_description = f.read()

def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]

reqs = parse_requirements('requirements.txt')


setup(name='phpbb-topic-post',
      version='0.9',
      description='PhpBB add topic and post',
      url='https://github.com/madyel/phpbb',
      author='MaDyEl',
      author_email='madyel83@tutanota.com',
      license='MIT',
      packages=['madyel', 'madyel.config'],
      install_requires=reqs,
      long_description=long_description,
      long_description_content_type='text/markdown'
      )