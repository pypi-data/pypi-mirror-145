import setuptools


long_description = open("README.md").read()
python_requires = '>=3'
install_requires = [
    'curlify',
    'pyunicore',
    'psutil'
]

setuptools.setup(
    name="pyunicoremanager",
    version="0.0.3",
    author="Aarón Pérez Martín",
    author_email="a.perez.martin@fz-juelich.de",
    description="Python wrapper of PyUnicore to deploy jobs on UNICORE systems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aperezmartin/PyUnicoreManager",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
