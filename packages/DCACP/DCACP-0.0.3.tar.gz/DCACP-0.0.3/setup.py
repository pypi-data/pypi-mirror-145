import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DCACP",
    version="0.0.3",
    author="ShijieZeng",
    author_email="zengshijie@stu.cdu.edu.cn",
    description="A Dyeing Clustering Algorithm based on Ant Colony Path-finding",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/firesaku/DCACP",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['matplotlib>=3.3.2', 'numpy==1.19.2', 'pandas>=1.1.3', 'scipy>=1.5.2', 'seaborn>=0.11.0'],
    python_requires='>=3'
)