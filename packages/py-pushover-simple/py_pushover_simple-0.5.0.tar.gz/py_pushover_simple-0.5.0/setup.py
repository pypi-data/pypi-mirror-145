import setuptools

with open("README.md", "r") as fh:
    readme = fh.read()

REPO = "https://github.com/prplecake/py_pushover_simple"

setuptools.setup(
    name="py_pushover_simple",
    version="0.5.0",
    author="Matthew Jorgensen",
    author_email="matthew@jrgnsn.net",
    description="A wrapper for sending push notifications with Pushover",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/prplecake/py_pushover_simple",
    project_urls={
        "Documentation": f"{REPO}/wiki",
        "Code": REPO,
        "Issue Tracker": f"{REPO}/issues",
    },
    packages=setuptools.find_packages(),
    classifiers=(
        "Development Status :: 3 - Alpha",
        "Environment :: Plugins",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Natural Language :: English",
        "Topic :: Communications",
        "Topic :: Utilities",
    ),
)
