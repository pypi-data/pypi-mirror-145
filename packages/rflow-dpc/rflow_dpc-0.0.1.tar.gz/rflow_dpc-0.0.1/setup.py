import setuptools


setuptools.setup(
    name="rflow_dpc",
    version="0.0.1",
    description ="Rflow Data Producer and Consumer",
    packages = setuptools.find_packages('src'),
    package_dir={'':'src'},
    author="LI, FUU",
    author_email = "rflowteam@rakuten.com",
    licence="",
    install_requires=['protobuf', 'grpcio']
)


# setuptools.setup(
#     name="rfdpc",
#     packages=setuptools.find_packages('src'),
#     package_dir={'':'src'},
#     author="Fuu, Li"
# )

