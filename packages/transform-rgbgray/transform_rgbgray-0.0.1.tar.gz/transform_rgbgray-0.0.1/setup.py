from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="transform_rgbgray",
    version="0.0.1",
    author="Jorge Magno",
    author_email="jorge.magnolm@gmail.com",
    description="Pacote de transformação de imagens",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JorgeMagno/image-processing-image-python",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)
