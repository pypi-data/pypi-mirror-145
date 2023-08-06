from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

with open('scrapy_newrabbit/VERSION','r')as f:
    version = f.read()

setup(
    name='scrapy_newrabbit',
    version=version,
    packages=find_packages(),
    author='LinShu',
    license='MIT',
    zip_safe=False,
    include_package_data=True,
    data_files=['scrapy_newrabbit/VERSION'],
    author_email='1419282435@qq.com',
    description='Scrapy_NewRabbit',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts':[
            'scrapy_newrabbit = scrapy_newrabbit.cmdline:execute'
        ]
    },
    python_requires='>=3.6',
)

