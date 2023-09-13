import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MEGworkshop2023", 
    version="0.1",
    author="Jeff Stout",
    author_email="stoutjd@nih.gov",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nih-megcore/MEG_workshop_2023",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: UNLICENSE",
        "Operating System :: Linux/Unix",
    ],
    python_requires='>3.8',
    install_requires=['mne', 'numpy', 'scipy', 'pandas', 'nibabel', 'nilearn', 'seaborn', 'mne_bids','nbdime'],
    scripts=[ ],
    )
