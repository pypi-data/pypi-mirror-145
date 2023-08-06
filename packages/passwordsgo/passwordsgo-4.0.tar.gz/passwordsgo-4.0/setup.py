import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="passwordsgo",
    version="4.0",
    author="Anish M",
    author_email="aneesh25861@gmail.com",
    description="A Highly Secure Quantum Safe password management tool done as student project in cryptography.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="GPLv3+",
    keywords = ['Password manager', 'cryptography','student project'],
    url="https://github.com/Anish-M-code/PyPass",
    packages=["passwordsgo"],
    classifiers=(
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python",
        "Topic :: Security :: Cryptography",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
    ),
    entry_points={"console_scripts": ["passwordsgo = passwordsgo:main",],},
)
