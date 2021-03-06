# cfutils

[![Readthedocs](https://readthedocs.org/projects/cfutils/badge/?version=latest)](https://cfutils.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://img.shields.io/travis/yech1990/cfutils.svg)](https://travis-ci.org/yech1990/cfutils)
[![Pypi Releases](https://img.shields.io/pypi/v/cfutils.svg)](https://pypi.python.org/pypi/cfutils)
[![Downloads](https://pepy.tech/badge/cfutils)](https://pepy.tech/project/cfutils)

**Chromatogram File Utils**

For Sanger sequencing data visualizing, alignment, mutation calling, and trimming etc.

## Demo

![plot chromatogram with mutation](https://raw.githubusercontent.com/yech1990/cfutils/master/data/plot.png)

> command to generate the demo above

```bash
cfutils mut --query ./data/B5-M13R_B07.ab1 --subject ./data/ref.fa --outdir ./data/ --plot
```

## How to install?

### form pypi

_(use this way ONLY, if you don't know what's going on)_

```bash
pip install --user cfutils
```

### manipulate the source code

- clone from github

```bash
git clone git@github.com:yech1990/cfutils.git
```

- install the dependence

```bash
make init
```

- do unittest

```bash
make test
```

## How to use?

- in the command line

```bash
cfutils mut --help
```

- or as a python module

```python
import cfutils as cf
```

## ChangeLog

- build as python package for pypi
- fix bug that highlighting wrong base

## TODO

- [ ] call mutation by alignment and plot Chromatogram graphic
- [ ] add a doc
- [x] change xaxis by peak location
- [ ] fix bug that chromatogram switch pos after trim
- [x] wrap as a cli app
- [ ] return quality score in output
- [ ] fix issue that selected base is not in the middle
- [ ] fix plot_chromatograph rendering bug

- [ ] add projection feature to make align and assemble possible
