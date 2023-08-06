from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='i2a_django_tools',
    version='2.0.2',
    description='Sdk for i2a django tools',
    long_description_content_type="text/markdown",
    long_description=README,
    license='MIT',
    packages=find_packages(),
    author='i2a Solutions Inc.',
    author_email='msyta@i2asolutions.com',
    keywords=['I2A Django Tools', 'I2A', 'Python 3', 'I2A Tools SDK'],
    download_url='https://pypi.org/project/i2a_django_tools/'
)

install_requires = [

]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
