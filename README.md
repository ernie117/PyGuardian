# PyGuardian

Soon-to-be python package for requesting tabulated character information from the Bungie API. You'll need a Bungie API key for this, set as environmental variable "BUNGIE_API". Until this is a proper package that can be installed with pip, you'll have to run  commands from inside the parent directory.

Alternatively run ```python -m site --user-site``` which will return a directory. Place the pyguardian repo in that directory, then you can run the command from anywhere

**On its first run PyGuardian will download Destiny 2 manifest data from the API, which is used as reference for item names like weapon and armour, then write it to json files.
PyGuardian checks if a manifest update is needed on every run, if there is an update it will download and overwrite the existing files** 
## Requirements

Install these requirements with pip:
`requests`
`python-dateutil`
`tabulate`

## Run with:

```python -m PyGuardian < psnname/xboxname/battleID > < playstation/xbox/pc > < eq/stats/playtime/last/vault/vault-name/vault-type/vault-tier > ```

For example, to get my stats it would be:

```python -m PyGuardian ernie#22462 pc stats ```

### Fluent Interface

PyGuardian also provides a fluent interface which can be used to request character, equipment and vault data directly from the Bungie API to use as you desire:

To return json data for all characters associated with ernie#22462:

```PyGuardian().api_key(<your_api_key>).gamertag("ernie#22462").platform("pc").fetch_character_json().print_character_json()```


## Things I want to do

* Write a setup.py
* Turn this into a fully-fledged python package
* Write docstrings for everything
* Develop fluent interface
