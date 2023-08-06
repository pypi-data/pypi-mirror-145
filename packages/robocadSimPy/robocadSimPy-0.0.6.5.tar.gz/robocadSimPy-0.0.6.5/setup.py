from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='robocadSimPy',
    version='0.0.6.5',
    description='python lib for robocadSim',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='https://readthedocs.org/projects/robocadsim/',
    author='Abdrakov Airat',
    author_email='abdrakovairat@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords=['simulator', 'robotics', 'robot', '3d'],
    packages=find_packages(),
    install_requires=['numpy', 'funcad']
)
