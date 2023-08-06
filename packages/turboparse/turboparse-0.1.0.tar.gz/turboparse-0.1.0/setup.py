from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='turboparse',
    packages=['turboparse'],
    version='0.1.0',
    license='MIT',
    description='Parse turbomole outputs and output json or yaml file',
    author='Shane M. Parker',
    author_email='shane.parker@case.edu',
    url='https://gitlab.com/team-parker/turboparse/',
    keywords=['Quantum Chemistry'],
    install_requires=[
        'pyyaml'
        ],
    entry_points = {
        'console_scripts' : [ 'turboparse=turboparse.parse:parse' ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Topic :: Scientific/Engineering :: Physics',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6'
        ]
)

