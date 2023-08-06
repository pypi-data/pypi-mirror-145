from setuptools import find_packages, setup

setup(
    name='cenao',
    version='0.1.0',
    url='https://gitlab.uwtech.org/uwtech/cenao',
    license='MIT',
    author='Roman Shishkin',
    author_email='spark@uwtech.org',
    description='Python framework for fast and async applications',
    project_urls={
        'Source': 'https://gitlab.uwtech.org/uwtech/cenao',
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.6',
    install_requires=[
        'aiohttp==3.8.1',
        'async-timeout==4.0.2',
        'PyYAML==6.0',
    ],
    extras_require={
        'redis': ['aioredis==1.3.1'],
    }
)
