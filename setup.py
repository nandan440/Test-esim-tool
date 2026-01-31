from setuptools import setup, find_packages

setup(
    name="esim-tools-manager",
    version="0.0.1",
    author="Aaruni",
    author_email="aaruni1saini@gmail.com",
    description="Automated Tool Manager for eSim",
    license="MIT",

    packages=find_packages(),

    entry_points={
        "console_scripts": [
            "esim-tools=esim_tool_manager.cli:main"
        ]
    },

    python_requires=">=3.8",

    install_requires=[
        "pyyaml",
        "requests"
    ],
    include_package_data=True,
)
