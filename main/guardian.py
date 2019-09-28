import json
from collections import namedtuple


Item = namedtuple("Item", "name, type, tier")
Character_description = namedtuple("Description", "gender, race, class_")


class Guardian:

    def __init__(self, init_dictionary):
        self.__dict__.update(init_dictionary)

    def __str__(self):
        return str(Character_description(self.get_gender(), self.get_race(), self.get_class()))

    def get_gamertag(self):
        return getattr(self, "_gamertag")

    def get_character_id(self):
        return getattr(self, "_character_id")

    def get_membership_id(self):
        return getattr(self, "_membership_id")

    def get_membership_type(self):
        return getattr(self, "_membership_type")

    def get_date_last_played(self):
        return getattr(self, "_date_last_played")

    def get_total_mins_played(self):
        return getattr(self, "_total_mins_played")

    def get_gender(self):
        return getattr(self, "_gender")

    def get_race(self):
        return getattr(self, "_race")

    def get_class(self):
        return getattr(self, "_class")

    def get_subclass(self):
        return getattr(self, "_subclass")

    def get_level(self):
        return getattr(self, "_level")

    def get_light(self):
        return getattr(self, "_light")

    def get_mobility(self):
        return getattr(self, "_mobility")

    def get_resilience(self):
        return getattr(self, "_resilience")

    def get_recovery(self):
        return getattr(self, "_recovery")

    def get_emblem_path(self):
        return getattr(self, "_emblem_path")

    def get_primary(self):
        return Item(*getattr(self, "_primary"))

    def get_secondary(self):
        return Item(*getattr(self, "_secondary"))

    def get_heavy(self):
        return Item(*getattr(self, "_heavy"))

    def get_helmet(self):
        return Item(*getattr(self, "_helmet"))

    def get_gauntlets(self):
        return Item(*getattr(self, "_gauntlets"))

    def get_chest(self):
        return Item(*getattr(self, "_chest"))

    def get_greaves(self):
        return Item(*getattr(self, "_greaves"))

    def get_class_item(self):
        return Item(*getattr(self, "_class_item"))

    def get_sparrow(self):
        return Item(*getattr(self, "_sparrow"))

    def get_ghost(self):
        return Item(*getattr(self, "_ghost"))

    def get_ship(self):
        return Item(*getattr(self, "_ship"))

