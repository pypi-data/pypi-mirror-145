from setuptools import setup

setup(
    name = 'iMVP-utils',
    author = 'Jianheng Liu, Jing Yao',
    author_email='jhfoxliu@gmail.com',
    url="https://github.com/jhfoxliu/iMVP",
    project_urls={
        "Bug Tracker": "https://github.com/jhfoxliu/issues",
    },
    description = 'Utils for interactive epitranscriptomic Motif Visualization and Sub-type Partitioning (iMVP).',
    version = '0.2.3',
    packages = ['iMVP_utils'],
    license = "MIT",
    scripts=["iMVP_viewer.py"],
    python_requires=">=3.6",
    install_requires = [
        "numpy>=1.20.0",
        "pandas>=1.3.4",
        "scipy>=1.5.1",
        "hdbscan>=0.8.27",
        "umap-learn>=0.5.2",
        "matplotlib>=3.2.2",
        "seaborn>=0.10.1",
        "scikit-learn>=0.23.1",
        "biopython>=1.77",
        "dash>=2.2.0",
        "dash-bio>=0.9.0",
        "imageio>=2.13.5",
        "weblogo>=3.7.0",
        "opencv-python>=4.5.5",
    ],
    package_data={"iMVP_utils": ["assets/*.css"]},

)