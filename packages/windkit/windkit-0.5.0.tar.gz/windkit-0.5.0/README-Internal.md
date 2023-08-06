# WindKit

This project provides common xarray data structures for several wind energy related data formats, as well as plotting and spatial manipulation routines.

## Downstream projects:

- [daTap](https://gitlab-internal.windenergy.dtu.dk/ram/software/tech-team/web-apps/daTap)
- [PyWAsP](https://gitlab-internal.windenergy.dtu.dk/ram/software/pywasp/pywasp)
- [PyWAsP Swarm](https://gitlab-internal.windenergy.dtu.dk/ram/software/pywasp/pywasp-swarm)
- [WindSider Validation](https://gitlab.windenergy.dtu.dk/windsider)

## Developer documentation

[Developer documentation](https://ram.pages-internal.windenergy.dtu.dk/software/pywasp/pywasp-developer-docs/) is maintained in the [Pywasp Developer Docs repository](https://gitlab-internal.windenergy.dtu.dk/ram/software/pywasp/pywasp-developer-docs) using mkdocs.

### Use of lock files

`conda-lock --mamba -f dev_env.yaml -p linux-64 -p osx-64 -p win-64`
`mamba create -n pywasp_env --file conda-lock_linux-64.lock`

## Build and deploy new version

```
export SETUPTOOLS_SCM_PRETEND_VERSION=<version>
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=<password>

# Create build environment
mamba create -n build boa build python=3.9
conda activate build

# Build & deploy Pypi
rm -r dist
python -m build
python3 -m twine upload dist/*

# Build & deploy conda
rm -r conda_build
export VERSION=<version>
time conda mambabuild -c https://conda.windenergy.dtu.dk/channel/open --output-folder conda_build  ./recipe

scp conda_build/*/*.tar.bz2 VIND-pWEBext01:~/.
ssh VIND-pWEBext01
  sudo mv *.tar.bz2 /srv/conda/open/noarch/.
  sudo chown 1000:1000 /srv/conda/open/noarch/*.tar.bz2
  docker exec -it ci_deploy /bin/bash
    su conda_deploy
    conda index ~/repos/open/
```
