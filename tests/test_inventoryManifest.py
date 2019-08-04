import json
import os
from operator import itemgetter
from pathlib import Path
from unittest import TestCase

from pyguardian.data_processing.hashes import InventoryManifest


class TestInventoryManifest(TestCase):
    # Read in dummy data
    with open(str(Path(__file__).parent) + "/resources/dummy_equip_data.json", "r") as f:
        equip_data = json.load(f)

    test_data_file = str(os.getcwd()) + "/resources/dummy_inventoryItemDefinition.json"

    test_eq_hashes = [
        [
            ["MALE", "EXO", "WARLOCK"],
            2712244741, 1887808042,
            1201830623, 381563628,
            3830828709, 3192591867,
            4178158375, 1549308050,
            813936739, 1363029408,
            2844014413
        ]
    ]

    test_item_result = ["Bygones", "Pulse Rifle", "Legendary"]

    vault_hashes = [
        4285666432, 2014411539, 4101386442, 1177810185, 2109561326, 950899352
    ]

    def test_get_full_item_details_eq_hashes(self):
        """
        Produces a list of lists, one containing a description
        of the character, the rest containing a name, type and
        rarity for each piece of equipment
        """
        manifest = InventoryManifest(self.test_eq_hashes, self.test_data_file)
        items = manifest.get_full_item_details()

        self.assertTrue(items)
        self.assertIsInstance(items, list)
        self.assertIsInstance(items[0], list)
        self.assertIsInstance(items[0][0], str)
        self.assertEqual(len(self.test_eq_hashes[0]), len(items))
        self.assertIn(self.test_item_result, items)

    def test_get_full_item_details_vault_sort_by_name(self):
        """
        passing the 'sort_by' argument with 'name' should sort
        the list by item name
        """
        manifest = InventoryManifest(self.test_eq_hashes, self.test_data_file)
        returned_items = manifest.get_full_item_details(sort_by="name")

        correctly_sorted_items = sorted(returned_items, key=itemgetter(0))
        incorrectly_sorted_items = sorted(returned_items, key=itemgetter(1))
        more_incorrectly_sorted_items = sorted(returned_items, key=itemgetter(2))

        self.assertTrue(returned_items)
        self.assertTrue(correctly_sorted_items)
        self.assertEqual(returned_items, correctly_sorted_items)
        self.assertNotEqual(returned_items, incorrectly_sorted_items)
        self.assertNotEqual(returned_items, more_incorrectly_sorted_items)

    def test_get_full_item_details_vault_sort_by_type(self):
        """
        passing the 'sort_by' argument with 'type' should sort
        the list by item type (pulse rifle, hand cannon, etc...)
        """
        manifest = InventoryManifest(self.test_eq_hashes, self.test_data_file)
        returned_items = manifest.get_full_item_details(sort_by="type")

        correctly_sorted_items = sorted(returned_items, key=itemgetter(1))
        incorrectly_sorted_items = sorted(returned_items, key=itemgetter(0))
        more_incorrectly_sorted_items = sorted(returned_items, key=itemgetter(2))

        self.assertTrue(returned_items)
        self.assertTrue(correctly_sorted_items)
        self.assertEqual(returned_items, correctly_sorted_items)
        self.assertNotEqual(returned_items, incorrectly_sorted_items)
        self.assertNotEqual(returned_items, more_incorrectly_sorted_items)

    def test_get_full_item_details_vault_sort_by_rarity(self):
        """
        passing the 'sort_by' argument with 'tier' should sort
        the list by item tier (rare, legendary, etc...)
        """
        manifest = InventoryManifest(self.test_eq_hashes, self.test_data_file)
        returned_items = manifest.get_full_item_details(sort_by="tier")

        correctly_sorted_items = sorted(returned_items, key=itemgetter(2))
        incorrectly_sorted_items = sorted(returned_items, key=itemgetter(1))
        more_incorrectly_sorted_items = sorted(returned_items, key=itemgetter(0))

        self.assertTrue(returned_items)
        self.assertTrue(correctly_sorted_items)
        self.assertEqual(returned_items, correctly_sorted_items)
        self.assertNotEqual(returned_items, incorrectly_sorted_items)
        self.assertNotEqual(returned_items, more_incorrectly_sorted_items)
