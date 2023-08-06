# flit_scm

A PEP 518 build backend that uses [`setuptools_scm`](https://github.com/pypa/setuptools_scm) to generate a version file from your version control system, then [`flit_core`](https://flit.readthedocs.io/en/latest/index.html) to build the package.

To use it, set the `build-system` table in your `pyproject.toml` to as follows:

```toml
[build-system]
requires = ["flit_scm"]
build-backend = "flit_scm:buildapi"
```

Flit and `setuptools_scm` can be configured as normal (refer to their documentation). Example:

```toml
[build-system]
requires = ["flit_scm"]
build-backend = "flit_scm:buildapi"

[tool.flit.sdist]
exclude = [".gitignore"]

[tool.setuptools_scm]
write_to = "src/_version.py"
```

