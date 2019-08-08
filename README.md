# PyGuardian

Soon-to-be python package for requesting tabulated character information from the Bungie API. You'll need a Bungie API key for this, set as environmental variable "BUNGIE_API". Until this is a proper package that can be installed with pip, you'll have to run  commands from inside the parent directory.

Alternatively run ```python -m site --user-site``` which will return a directory. Place the pyguardian repo in that directory, then you can run the command from anywhere

## Run with:

> python -m pyguardian < psnname/xboxname/battleID > < playstation/xbox/pc > < eq/stats/playtime/last/vault/vault-name/vault-type/vault-tier >

For example, to get my stats it would be:

> python -m pyguardian ernie#22462 pc stats

## Things I want to do

* Write a setup.py
* Turn this into a fully-fledged python package
* Write docstrings for everything
