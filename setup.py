from setuptools import setup


long_description = ''
# Get the long description from the README file
with open('README.rst', 'r') as f:
    long_description = f.read()

setup(
    name='ozpy',
    version='1.0.1',
    license='GPL',
    long_description=long_description,
    url='https://github.com/iomarmochtar/ozpy',
    author='Imam Omar Mochtar',
    author_email='iomarmochtar@gmail.com',
    packages=['ozpy'],
    keywords='Zimbra Python library',
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.7',
        'Natural Language :: English',
    ]
)
