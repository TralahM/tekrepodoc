<img src="https://img.shields.io/github/license/TralahM/tekrepodoc"> <img src="https://img.shields.io/github/last-commit/TralahM/tekrepodoc"> <img src="https://img.shields.io/github/contributors/TralahM/tekrepodoc"> <img src="https://img.shields.io/github/issues-pr-raw/TralahM/tekrepodoc?color=blue"> <img src="https://img.shields.io/github/issues-pr-closed-raw/TralahM/tekrepodoc?color=red"> <img src="https://img.shields.io/github/issues-raw/TralahM/tekrepodoc?color=green"> <img src="https://img.shields.io/github/issues-closed-raw/TralahM/tekrepodoc?color=yellow"> <img src="https://img.shields.io/github/forks/TralahM/tekrepodoc?label=Forks&style=social"> <img src="https://img.shields.io/github/forks/TralahM/tekrepodoc?label=Forks&style=social"> <img src="https://img.shields.io/github/stars/TralahM/tekrepodoc?style=social"> <img src="https://img.shields.io/github/watchers/TralahM/tekrepodoc?label=Watch&style=social"> <img src="https://img.shields.io/github/downloads/TralahM/tekrepodoc/total"> <img src="https://img.shields.io/github/repo-size/TralahM/tekrepodoc"> <img src="https://img.shields.io/github/languages/count/TralahM/tekrepodoc"> <img src="https://img.shields.io/github/v/tag/TralahM/tekrepodoc"> <img src="https://img.shields.io/readthedocs/tekrepodoc">
<img src="https://img.shields.io/pypi/v/tekrepodoc"> <img src="https://img.shields.io/pypi/pyversions/tekrepodoc"> <img src="https://img.shields.io/pypi/wheel/tekrepodoc"> <img src="https://img.shields.io/pypi/status/tekrepodoc?label=pypi%20status"> <img src="https://img.shields.io/pypi/format/tekrepodoc?label=pypi%20format">

# tekrepodoc
> Utility Tool to Generate Common Project Files using sensible templates every one can agree on. Useful for Git Repositories, Supports Sphinx templates, Community Health Files, READMEs, pypi project configurations.


---

### Table of Contents
- [QuickStart](#QuickStart)
- [Documentation/Usage](#Documentation)
- [Contributing](#Contributing)
- [Credits](#Credits)

---
## QuickStart
#### Installation

```console
pip install tekrepodoc
```
#### From Source
```console
git clone https://github.com/TralahM/tekrepodoc
cd tekrepodoc

python setup.py bdist_wheel
pip install -e .

```
---

## CLI Usage
In terminal type
```console
repodoc -h
```

```
usage: repodoc [-h] [-u] [-bc] [-zc] [-vv] [-v]
               {get_vars,config,licence,readme,community_health,comh,ch,pypi_project,pypi,sphinx_docs,docs,sphinx,dot_files,dots}
               ...

options:
  -h, --help            show this help message and exit
  -u, --use-config-file
                        use config file for template variables.
  -bc, --bash-completion
                        Print Bash Completion Script.
  -zc, --zsh-completion
                        Print ZSH Completion Script.
  -vv, --verbose        Turn on Verbose Mode.
  -v, --version         show program's version number and exit

subcommands:
  {get_vars,config,licence,readme,community_health,comh,ch,pypi_project,pypi,sphinx_docs,docs,sphinx,dot_files,dots}
    get_vars            Return all variables for the given template.
    config              Configure Subcommand to init,set,get,list configs.
    licence             Generate Licence Command.
    readme              Generate README command.
    community_health (comh, ch)
                        Generate Community Health Guidelines.
    pypi_project (pypi)
                        Generate Pypi Manifest,setup.cfg,setup.py Command.
    sphinx_docs (docs, sphinx)
                        Generate Sphinx Documentation Templates.
    dot_files (dots)    Generate all dot files
                        .gitignore,.gitattributes,.mailmap.

Author: Tralah M Brian (TralahM) <musyoki.brian@tralahtek.com>. Project:
<https://github.com/TralahM/tekrepodoc>
```

## Documentation

[![Documentation](https://img.shields.io/badge/Docs-tekrepodoc-blue.svg?style=for-the-badge)](https://tekrepodoc.readthedocs.io)


#### API Reference

---
## Contributing

---

## Credits
[![TralahTek](https://img.shields.io/badge/Organization-TralahTek-black.svg?style=for-the-badge&logo=github)](https://github.com/TralahTek)
[![TralahM](https://img.shields.io/badge/Engineer-TralahM-blue.svg?style=for-the-badge&logo=github)](https://github.com/TralahM)
[![TralahM](https://img.shields.io/badge/Maintainer-TralahM-green.svg?style=for-the-badge&logo=github)](https://github.com/TralahM)



[![](https://img.shields.io/badge/Github-TralahM-green?style=for-the-badge&logo=github)](https://github.com/TralahM)
[![](https://img.shields.io/badge/Twitter-%40tralahtek-blue?style=for-the-badge&logo=twitter)](https://twitter.com/TralahM)
[![TralahM](https://img.shields.io/badge/Kaggle-TralahM-purple.svg?style=for-the-badge&logo=kaggle)](https://kaggle.com/TralahM)
[![TralahM](https://img.shields.io/badge/LinkedIn-TralahM-white.svg?style=for-the-badge&logo=linkedin)](https://linkedin.com/in/TralahM)


[![Blog](https://img.shields.io/badge/Blog-tralahm.tralahtek.com-blue.svg?style=for-the-badge&logo=rss)](https://tralahm.tralahtek.com)

[![TralahTek](https://img.shields.io/badge/Organization-TralahTek-cyan.svg?style=for-the-badge)](https://org.tralahtek.com)
---
