import unittest
import os
import shutil
from src.storage import versioning

class TestModelVersioning(unittest.TestCase):
    def setUp(self):
        self.registry_path = versioning.REGISTRY_PATH
        self.backup_path = self.registry_path + ".bak"
        # Always clear registry before each test
        if os.path.exists(self.registry_path):
            os.remove(self.registry_path)

    def tearDown(self):
        import os
        if os.path.exists(self.backup_path):
            os.remove(self.backup_path)
        if os.path.exists(self.registry_path):
            os.remove(self.registry_path)

    def test_register_and_list(self):
        v = versioning.register_model("path/to/model", {"r":1}, {"top1":0.9}, status="active")
        models = versioning.list_models()
        self.assertTrue(any(m["version"] == v for m in models))
        self.assertEqual(models[-1]["status"], "active")

    def test_atomicity(self):
        # Register two models and check both exist
        v1 = versioning.register_model("path/1", {"r":1}, {"top1":0.8}, status="active")
        v2 = versioning.register_model("path/2", {"r":2}, {"top1":0.9}, status="active")
        models = versioning.list_models()
        self.assertTrue(any(m["version"] == v1 for m in models))
        self.assertTrue(any(m["version"] == v2 for m in models))

    def test_validation(self):
        # Should raise if missing keys
        bad_entry = {"foo": "bar"}
        with self.assertRaises(ValueError):
            versioning.validate_entry(bad_entry)

    def test_set_active_and_rollback(self):
        v1 = versioning.register_model("path/1", {"r":1}, {"top1":0.8}, status="active")
        v2 = versioning.register_model("path/2", {"r":2}, {"top1":0.9}, status="active")
        versioning.set_active(v1)
        models = versioning.list_models()
        active = [m for m in models if m["status"] == "active"]
        self.assertEqual(len(active), 1)
        self.assertEqual(active[0]["version"], v1)

if __name__ == "__main__":
    unittest.main()