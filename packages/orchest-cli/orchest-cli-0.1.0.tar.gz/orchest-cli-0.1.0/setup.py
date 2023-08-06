import setuptools

setuptools.setup(
    name="orchest-cli",
    description="CLI for Orchest",
    version="0.1.0",
    license="Apache 2.0",
    author="Rick Lamers",
    author_email="rick@orchest.io",
    install_requires=[
        "click==8.0.4",
        "kubernetes==21.7.0",
    ],
    keywords="orchest",
    url="https://github.com/orchest/orchest",
    project_urls={
        "Documentation": (
            "https://docs.orchest.io/en/stable/"
        ),
        "Source Code": (
            "https://github.com/orchest/orchest"
        ),
    },
    classifiers=[
        "Environment :: Console",
        "Topic :: Utilities",
    ],
)
