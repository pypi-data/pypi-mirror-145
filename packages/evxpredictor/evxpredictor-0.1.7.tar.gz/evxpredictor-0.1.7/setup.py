try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

setup(
    name='evxpredictor',
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    version='0.1.7',
    description='A package for predicting buy and sell signals',
    license='MIT',
    author='Nicolus Rotich',
    author_email='nicholas.rotich@gmail.com',
    install_requires=[
    	"setuptools>=58.1.0",
    	"wheel>=0.37.1",
    	"keras==2.8.0",
    	"tensorflow>=2.8.0",
    	"scikit-learn>=1.0.2",
    	"scipy>=1.8.0",
    	"h5py>=3.6.0",
        "fire"
    ],
    url='https://nkrtech.com',
    download_url='https://github.com/moinonin/evxpredictor/archive/refs/heads/main.zip',
    classifiers=[
        'License :: OSI Approved :: MIT License',
    ],
)
