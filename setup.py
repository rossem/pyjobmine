from setuptools import setup, find_packages


def read_file(name):
    with open(name) as fd:
        return fd.read()


setup(
    name='pyjobmine',
    version=0.1,
    description='Unofficial Python API for JobMine',
    long_description=read_file('README.md'),
    url='https://github.com/rossem/JobMine-API',
    author='Rostislav Semenov',
    author_email='rrsbrg@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='python api for jobmine',
    packages=find_packages(),
    install_requires=read_file('requirements.txt').splitlines()
)
