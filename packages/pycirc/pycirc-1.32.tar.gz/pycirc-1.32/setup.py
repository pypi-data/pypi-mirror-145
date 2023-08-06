from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='pycirc',
    version='1.32',
    description='Python logic circuit modeling and simulation',
    keywords='digital circuit logic modeling simulation',
    author='Samy Zafrany',
    url='https://www.samyzaf.com/pycirc/pycirc.html',
    author_email='samyz@technion.ac.il',
    license='MIT',
    packages=['pycirc'],
    install_requires=['networkx'],
    zip_safe=False,
)

