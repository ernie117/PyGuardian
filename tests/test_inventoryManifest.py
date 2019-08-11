from operator import itemgetter
from unittest import TestCase
from unittest.mock import patch

from pyguardian.data_processing.hashes import InventoryManifest
from pyguardian.tests.resources import test_constants
from pyguardian.tests.resources.mock_classes import MockInventoryDefinition


class TestInventoryManifest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_data_file = test_constants.TEST_DATA_FILE
        cls.test_eq_hashes = test_constants.TEST_EQ_HASHES
        cls.test_item_result = test_constants.TEST_ITEM_RESULT
        cls.vault_hashes = test_constants.VAULT_HASHES

    def test_get_full_item_details_eq_hashes(self):
        manifest = InventoryManifest(self.test_eq_hashes, self.test_data_file)
        items = manifest.get_full_item_details()

        self.assertTrue(items)
        self.assertIsInstance(items, list)
        self.assertIsInstance(items[0], list)
        self.assertIsInstance(items[0][0], str)
        self.assertEqual(len(self.test_eq_hashes[0]), len(items))
        self.assertIn(self.test_item_result, items)

    def test_get_full_item_details_vault_sort_by_name(self):
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

    @patch("builtins.open")
    @patch("json.load", return_value=MockInventoryDefinition().json())
    def test_get_full_item_details_alternate_json_structure(self, mock_load, mock_open):
        manifest = InventoryManifest(self.test_eq_hashes)
        returned_items = manifest.get_full_item_details()

        self.assertTrue(returned_items)
        self.assertIsInstance(returned_items, list)
        self.assertIsInstance(returned_items[0], list)
        self.assertIsInstance(returned_items[0][0], str)
        self.assertIn(["Dummy name", "", ""], returned_items)
