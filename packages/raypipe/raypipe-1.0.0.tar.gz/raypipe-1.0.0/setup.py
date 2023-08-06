import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="raypipe",
    version="1.0.0",
    author="Billy Yan",
    author_email="",
    description="Easy implementation and abstraction for train and deploy model on ray cluster",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/billyyann/RayPipe",
    packages=setuptools.find_packages(),
    install_requires=['tensorflow-cpu==2.3.0'],
    entry_points={
        'console_scripts': [
        ],
    },
    setup_requires=[
        # 'pytest-runner==3.0',
        # setuptools需要使用50.0.0以上版本，否则执行pytest的时候，无法从我司自己的pypi里下载
        'setuptools>=50.0.0',
        'ruamel.yaml',
        'wheel'
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)