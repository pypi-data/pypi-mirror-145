import setuptools
import os
try:
    from sphinx.setup_command import BuildDoc
    cmdclass = {"build_sphinx": BuildDoc}
except ModuleNotFoundError:
    pass

def long_desc(path_to_md):
    """
    Use markdown for description on devpi server.
    """
    with open(path_to_md, "r") as _fh:
        return _fh.read()

setuptools.setup(
  name = "csv-jsonl",
  version = "0.1.3",
  description = "Leverage the built-in python csv module to write files in jsonl format",
  long_description=long_desc("README.md"),
  long_description_content_type="text/markdown", # use mimetype!
  py_modules=["csv_jsonl"],
  platforms="any",
  author = "Doug Shawhan",
  author_email = "doug.shawhan@gmail.com",
  url="https://gitlab.com/doug.shawhan/csv-jsonl",
    project_urls={
        "Bug Tracker": "https://gitlab.com/doug.shawhan/csv-jsonl/issues",
        "Source Code": "https://gitlab.com/doug.shawhan/csv-jsonl/tree/main",
        "Development Version": "https://gitlab.com/doug.shawhan/csv-jsonl/tree/dev",
        "Documentation": "https://csv-jsonl.readthedocs.io",
    },

  keywords = ["python", "jsonl", "jsonlines", "csv", "bigquery"],
  install_requires= [],
  python_requires=">=3.7",
  classifiers = [
      "Programming Language :: Python :: 3",
      "Programming Language :: Python :: 3.7",
      "Programming Language :: Python :: 3.8",
      "Programming Language :: Python :: 3.9",
      "Programming Language :: Python :: 3.10",
      "Intended Audience :: Developers",
      "Operating System :: OS Independent",
      "Topic :: Software Development :: Libraries :: Python Modules",
  ],
  include_package_data=True,
  packages=setuptools.find_packages(),
  zip_safe=True
)
