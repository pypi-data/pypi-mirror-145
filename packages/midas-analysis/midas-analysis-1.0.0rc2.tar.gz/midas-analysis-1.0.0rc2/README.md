# MIDAS Analysis Tool

## Description
This package contains the analysis tool of MIDAS. It allows to perform a basic analysis of the simulation database create by the `midas-store` module.

This package is intended to be used with MIDAS and can be used with the `midasctl` command line tool.

## Installation
This package will usually be installed automatically together with `midas-mosaik`. It is available on pypi, so you can install it manually with

```bash
pip install midas-analysis
```

## Usage
The complete documentation is available at https://midas-mosaik.gitlab.io/midas.

To start the analysis, execute following command

```bash
midasctl analyze path/to/my_db.hdf5
```

where `path/to/my_db.hdf5` usually is the output directory defined in the runtime config. A new folder will be created with the same name as the database file and inside that folder you will find the analysis results.

## License
This software is released under the GNU Lesser General Public License (LGPL). See the license file for more information about the details.
