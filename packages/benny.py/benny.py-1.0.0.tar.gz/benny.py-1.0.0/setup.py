from setuptools import setup

readme = """
# benny.py
A Python wrapper for Benny's API.

### Install
> ```bash
> $ pip install benny.py
> ```

### Example
> ```python
> import benny
> 
> client = benny.Client()
> 
> cat_image = client.cat()
> dog_image = client.dog()
> 
> print(cat_image, dog_image)
> ```
"""

setup(
    name='benny.py',
    version='1.0.0',
    description='A Python wrapper for Benny\'s API.',
    requires=['requests'],
    packages=['benny', 'benny.utils'],
    author='Ben Tettmar',
    url='https://github.com/bentettmar/benny.py',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ],
    long_description=readme,
    long_description_content_type='text/markdown'
)