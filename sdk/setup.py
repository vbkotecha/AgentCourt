#!/usr/bin/env python3
"""
AgentCourt Python SDK — setup.py for PyPI publishing
"""
from setuptools import setup

setup(
    name="agentcourt",
    version="1.1.0",
    description="Policy-driven dispute resolution API client for agent commerce",
    long_description=open("README.md").read() if __import__('os').path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    author="Vivek Kotecha",
    author_email="noreply@github.com",
    url="https://github.com/vbkotecha/agentcourt-api",
    license="MIT",
    python_requires=">=3.8",
    install_requires=[],  # zero dependencies
    py_modules=["agentcourt_python_sdk"],
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
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
