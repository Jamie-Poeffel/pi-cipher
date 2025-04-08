from setuptools import setup, find_packages

setup(
    name='pi_cipher',
    version='2.0.0',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'pi-cipher=cli:main',
        ],
    },
    author='Jamie Poeffel',
    description='Pi Cipher v2.0 - Quantum Ready Kryptotool',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/Jamie-Poeffel/pi_cipher',
    classifiers=[
        'Programming Language :: Python :: 2',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)
