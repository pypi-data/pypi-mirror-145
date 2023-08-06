import setuptools

with open("README.md", "r") as f:
    readme = f.read()

setuptools.setup(
    name="alma-hilse",
    version="0.3.1",
    description="ALMA Hardware-In-the-Loop Simulation Environment monitoring and verification package",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Jose L. Ortiz / ADE",
    author_email='jose.ortiz@alma.cl',
    url="https://bitbucket.sco.alma.cl/projects/ESG/repos/alma-hilse",
    packages=setuptools.find_packages(include=['alma_hilse', 'alma_hilse.*']),
    package_data={"alma_hilse": ["resources/*"]},
    entry_points={
        "console_scripts": [
            "alma-hilse=alma_hilse.__main__:main",
            "alma-hilse-lftrr=alma_hilse.__main__:status_lftrr",
            "alma-hilse-drxs=alma_hilse.__main__:status_drx"
        ],
    },
    license="MIT",
    install_requires=[
        "click==8.0.4",
        "typer==0.4.0",
        "rich==12.0.0"
    ],
    extras_require={
        "test": ["pytest"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
