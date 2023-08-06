import setuptools

with open("README.md","r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="project4bim2022_g2",
    version="0.0.1",
    author="Team2",
    author_email="seungyun.shin@insa-lyon.fr",
    description="A example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ruthh1/Projet-4bim",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
            ],
    packages=["Project4bim2022_g2"],
    package_data={'project4bim2022_g2':['model_vae/*/*']},
    include_package_data=True,
    python_requires= ">=3.6",

)