from setuptools import setup


# Get the long description from the README file
with open('README.rst', 'r') as f:
    long_description = f.read()

setup(
    name='ozpy',
    version='0.5',
    license='GPL',
    long_description=long_description,
    url='https://github.com/iomarmochtar/ozpy',
    author='Imam Omar Mochtar',
    author_email='iomarmochtar@gmail.com',
    install_requires=['requests'],
    packages=['ozpy'],
    keywords='Zimbra Python library',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2.7',
        'Natural Language :: English',
    ]
)
