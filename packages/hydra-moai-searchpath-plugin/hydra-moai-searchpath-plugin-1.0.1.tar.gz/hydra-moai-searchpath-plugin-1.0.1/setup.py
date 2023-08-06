from setuptools import (
    find_namespace_packages, 
    setup
)

with open("README.md", "r") as fh:
    LONG_DESC = fh.read()
    setup(
        name="hydra-moai-searchpath-plugin",
        version="1.0.1",
        author="AI-in-Motion Team",
        author_email="moai@ai-in-motion.dev",
        description="moai Hydra SearchPath plugin",
        long_description=LONG_DESC,
        long_description_content_type="text/markdown",
        url="https://github.com/ai-in-motion/moai",
        packages=find_namespace_packages(include=["hydra_plugins.*"]),
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Intended Audience :: Science/Research",
            "Programming Language :: Python :: 3.7",
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: OS Independent",
            "Topic :: Scientific/Engineering :: Artificial Intelligence",
            "Topic :: Software Development :: Libraries",
            "Topic :: Software Development :: Libraries :: Python Modules",
        ],   
        install_requires=[
            "hydra-core==1.0.*",
            "moai-mdk",            
        ],
        include_package_data=False,
    )