# secure-config-manager

## Description
Secure ConfigManager offers splitting your JSON config files into two parts.

We suggest one main `config.json` file that can be safely checked out to version control system. This can contain default values or a sample config structure for reference. The second one would be `config_override.json`, containing secret tokens or environment-dependent values.

Data in `config_override.json` is assumed to be more relevant, hence if the value is present in both configs, we choose config_override.

## Usage
```
from secure_config_manager import ConfigManager

config_manager = ConfigManager()
config_manager.

>>>
```

## Notes:
* ConfigManager is a singleton class
* ConfigManager is application-agnostic and can be used in any Python 3.x project of your choice