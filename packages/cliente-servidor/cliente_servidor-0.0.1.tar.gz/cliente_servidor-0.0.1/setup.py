from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_descripiton = f.read()


setup(
    name="cliente_servidor",
    version="0.0.1",
    author="Yan Vinícius",
    description="Conexão cliente/servidor utilizando UDP",
    long_description=page_descripiton,
    long_description_content_type="text/markdown"

)
