import setuptools


setuptools.setup(
    name="oktagon-python",
    version="0.0.7",
    author="Made.com Tech Team",
    author_email="andrii.piratovskyi@made.com",
    description="Python utility package for verifying & decoding OKTA tokens",
    url="https://github.com/madedotcom/oktagon-python",
    install_requires=[
        "okta_jwt_verifier",
        "starlette",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    package_data={"oktagon_python": ["py.typed"]},
    python_requires=">=3.6",
)
