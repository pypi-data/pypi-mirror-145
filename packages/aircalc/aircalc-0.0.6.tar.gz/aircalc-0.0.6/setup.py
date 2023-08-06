import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aircalc",
    version="0.0.6",
    author="yoshiyasu takefuji",
    author_email="takefuji@keio.jp",
    description="aircalc: calculate a math expression by five fingers in air.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ytakefuji/air_calculator",
    project_urls={
        "Bug Tracker": "https://github.com/ytakefuji/air_calculator",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['aircalc'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    entry_points = {
        'console_scripts': [
            'aircalc = aircalc:main'
        ]
    },
)
