from setuptools import setup, find_packages

setup(
    name='deepsport_utilities',
    author='Gabriel Van Zandycke',
    author_email="gabriel.vanzandycke@uclouvain.be",
    url="https://gitlab.com/deepsport/deepsport_utilities",
    licence="LGPL",
    python_requires='>=3.8',
    description="",
    version='4.0.10',
    packages=find_packages(),
    install_requires=[
        "numpy",
        "scipy",
        "opencv-python",
        "imageio",
        "m3u8",
        "requests",
        "calib3d>=2.5.1",
        "mlworkflow>=0.3.9",
        "pytest",
        "shapely",
        "scikit-image",
        "python-dotenv",
        "aleatorpy"
    ],
)
