from setuptools import setup

name = "types-freezegun"
description = "Typing stubs for freezegun"
long_description = '''
## Typing stubs for freezegun

This is a PEP 561 type stub package for the `freezegun` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `freezegun`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/freezegun. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `ec27c00ca220c501a55e51617117f5b2d60fc06c`.
'''.lstrip()

setup(name=name,
      version="1.1.8",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/freezegun.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['freezegun-stubs'],
      package_data={'freezegun-stubs': ['__init__.pyi', 'api.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Stubs Only",
      ]
)
