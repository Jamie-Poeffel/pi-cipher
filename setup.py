from setuptools import setup, find_packages

setup(
    name='pi_cipher',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'pi-cipher=cli:main',
        ],
    },
    author='Dein Name',
    description='Verschlüsselungstool basierend auf Pi mit Dummy-Daten und Redundanz',
    license='MIT',
)
