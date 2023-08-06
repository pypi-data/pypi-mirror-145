<p align="center">
  <a aria-label="License" href="https://github.com/cloudFPGA/trieres/blob/master/LICENSE">
    <img alt="" src="https://img.shields.io/github/license/cloudFPGA/trieres?style=for-the-badge&labelColor=000000">
  </a>
  <a aria-label="PyPi" href="https://pypi.org/project/trieres/">
    <img alt="" src="https://img.shields.io/pypi/v/trieres?style=for-the-badge&labelColor=000000">
  </a>
  <a aria-label="Python" href="#trieres">
    <img alt="" src="https://img.shields.io/pypi/pyversions/trieres?style=for-the-badge&labelColor=000000">
  </a>
</p>

# trieres
This is a python module enabling the remote execution of accelerated functions on the [cloudFPGA platform](https://www.zurich.ibm.com/cci/cloudFPGA/).

## Workflow

```
git clone --depth 1 --recursive git@github.com:cloudFPGA/trieres.git
cd trieres  
make env
source venv/bin/activate
make genlib
make dist 
make upload
```
