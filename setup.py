from setuptools import setup, find_packages

setup(
    name="checkpoint_restart",
    version="0.1.0",
    packages=find_packages(),
    scripts=[
        "job_monitoring/check_hang.py",
        "job_monitoring/check_nan.py",
        "utils/get_healthy_nodes.sh",
        "utils/launcher.sh",
        "utils/flush.sh",         
    ],
    author="Huihuo Zheng",
    author_email="huihuo.zheng@anl.gov",
    description="A package for checkpoint/restart tests on Exascale computing systems.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/argonne-lcf/checkpoint_restart",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
