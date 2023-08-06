import setuptools

setuptools.setup(
    license='MIT',
    name="jcrs",
    version="1.0",
    author="JenCat",
    author_email="gubenkovalik@gmail.com",
    description="JenCat TCP Relay Server",
    long_description='JenCat TCP Relay Server',
    packages=["jcrs"],
    keywords='tcp relay server',
    include_package_data=True,
    python_requires='>=3.8',
    install_requires=[

    ],
    entry_points={
        'console_scripts': [
            'jcrs=jcrs.server:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)