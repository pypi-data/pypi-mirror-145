from setuptools import find_packages, setup

setup(
    name='PyCyberUtils',
    packages=find_packages(include=['PyCyberUtils']),
    version='0.3.5',
    description='Hacking Team main utils library',
    author='ConnorDev',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner', 'requests', 'coloredlogs'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)