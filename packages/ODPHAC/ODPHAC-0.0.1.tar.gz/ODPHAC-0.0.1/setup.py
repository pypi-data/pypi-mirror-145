import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ODPHAC",
    version="0.0.1",
    author="yf_123",
    author_email="wangyuefei@cdu.edu.cn",
    description="An outlier detection strategy for spatial free path-finding based on hierarchical ant colonies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YF-W/ODPHAC",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['matplotlib>=3.3.2', 'numpy==1.19.2', 'scipy>=1.5.2'],
    python_requires='>=3'
)