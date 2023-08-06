from setuptools import setup, find_packages

setup(
    name='scPrivacy',
    version='1.0',
    description='scPrivacy',
    url='https://github.com/bm2-lab/scPrivacy',
    packages=find_packages(),
    install_requires=[
        'torch>=1.2',
        'pandas>=0.23.4',
        'numpy>=1.12.0',
        'scipy>=1.0.0',
        'tqdm>=4.28.1',
        'scanpy>=1.4.4.post1',
        'crypten>=0.1'
    ],
    author='Shaoqi Chen',
    author_email='csq_@tongji.edu.cn',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
