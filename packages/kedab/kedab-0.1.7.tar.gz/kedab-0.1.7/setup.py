from setuptools import setup

setup(
    name='kedab',
    version='0.1.7',    
    description="Basic library for Machine learning operations",
    author="Busenur Aktilav, Dalia Dawod, Kerem Comert",
    license='MIT',
    packages=['kedab'],
    install_requires=["numpy", "pandas", "dotmap", "matplotlib"],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',  
        'Operating System :: OS Independent',        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ],
)
