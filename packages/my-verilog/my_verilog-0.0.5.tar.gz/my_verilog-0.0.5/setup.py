import setuptools

setuptools.setup(
    name="my_verilog",
    version="0.0.5",
    author="zyz",
    author_email="940746691@qq.com",
    description="a verilog package based on python3",
    packages=setuptools.find_packages(),
    install_requires=[
        'pyverilog>=1.3.0'
    ],
)
