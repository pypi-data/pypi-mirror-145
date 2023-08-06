import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    readme_content = fh.read().strip()

setuptools.setup(
    name="pcl2_joke_cui",
    version="0.0.2",
    author="cui",
    author_email="cui.ding@uzh.com",
    description="creating CLI for processing joke.",
    long_description=readme_content,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="MIT",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    package_data={
    	"": ["*.txt"],
    	"clipkg": ["data/*"],
    	},
    python_requires=">=3.6",
)