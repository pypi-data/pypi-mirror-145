import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name='ovex_py',
    version='0.0.1',    
    description='A package to interact with OVEX API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Quirky-Fox/OVEX-py',
    download_url = 'https://github.com/Quirky-Fox/OVEX-py/archive/refs/tags/v0.0.1.tar.gz',
    python_requires=">=3.6",
    author='Duncan Andrew',
    author_email='duncan@lumina-x.com',
    license='MIT',
    packages=['ovex_python'],
    install_requires=['requests'],
    keywords='OVEX cryptocurrency exchange API',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Office/Business :: Financial',
        'Topic :: Utilities',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)