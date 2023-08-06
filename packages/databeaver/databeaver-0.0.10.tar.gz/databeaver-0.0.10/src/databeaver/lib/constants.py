from enum import Enum


class DropStyle(Enum):
    """
    Represents the three approaches to handling the dropping of objects
    """
    # No objects will be dropped, User sql scripts will take care of the dropping of objects
    NONE = 1

    # The schema will be dropped and recreated before models are generated. This method prevents any objects from
    # accumulating in the schema
    SCHEMA = 2

    # The table will be dropped before the model is generated
    TABLE = 3


class ConfigFormats(Enum):
    # cfg/ini format
    INI = 1

    # JSON format
    JSON = 2

    # TOML format
    TOML = 3

    # YAML format
    YAML = 4
