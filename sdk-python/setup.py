from setuptools import setup, find_packages

setup(
    name="agentcourt",
    version="1.0.0",
    description="Policy-driven dispute resolution SDK for AI agent commerce",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Vivek Kotecha",
    author_email="vbkotecha@gmail.com",
    url="https://github.com/vbkotecha/agentcourt-api",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="agentcourt dispute resolution agent commerce x402 base usdc arbitration mcp",
)
