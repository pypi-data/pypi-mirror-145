# Supporting python modules for the LatticeDNAOrigami simulation program

Python package for analysis, visualization, and support for the LatticeDNAOrigami simulation program.
This package is part of the replication package for Ref. 1.

Some example scripts for creating plots are provided in the [`scripts`](scripts/) directory.

## Installation

This package was developed and used on Linux.
[It is available on the PyPI respository](https://pypi.org/project/origampy/).
It can be installed by running
```
pip install origamipy
```
If you do not have root access and it does not automatically default to installing locally, the `--user` flag may be used.
To install directly from this repository, run
```
python -m build
pip install dist/origamipy-[current version]-py3-none-any.whl
```
To run the above, it may be necessary to update a few packages:
```
python3 -m pip install --upgrade pip setuptools wheel
```

For more information on building and installing python packages, see the documentation from the [Python Packaging Authority](https://packaging.python.org/en/latest/).

## References

[1] A. Cumberworth, D. Frenkel, and A. Reinhardt, Simulations of DNA-origami self-assembly reveal design-dependent nucleation barriers.

## Links

[LatticeDNAOrigami](https://github.com/cumberworth/LatticeDNAOrigami)

[Python Packaging Authority](https://packaging.python.org/en/latest/)
