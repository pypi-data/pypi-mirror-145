import os
from setuptools import setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='bci-stream',
    version='0.0',
    packages=[],
    author='Yeison Cardona',
    author_email='yencardonaal@unal.edu.co',
    maintainer='Yeison Cardona',
    maintainer_email='yencardonaal@unal.edu.co',

    download_url='https://github.com/UN-GCPDS/',

    install_requires=[],

    python_requires='>=3.9',

    include_package_data=True,
    license='BSD-2-Clause',
    description="",
    long_description='',
    long_description_content_type='text/markdown',

    classifiers=[
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.8',
    ],


)
