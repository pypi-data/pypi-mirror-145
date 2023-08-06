""" test data

   isort:skip_file
"""
import json
import os
import sys
import unittest
from mock import patch
from ciocore import data

PROJECTS = [
    "Deadpool",
    "Harry Potter & the chamber of secrets",
    "Captain Corelli's Mandolin",
    "Gone with the Wind"
]

LIN_INSTANCE_TYPES = [
    {
        "cores": 8,
        "memory": 30.0,
        "description": "8 core, 30GB Mem",
        "name": "n1-standard-8",
        "operating_system": "linux"
    },
    {
        "cores": 64,
        "memory": 416.0,
        "description": "64 core, 416GB Mem",
        "name": "n1-highmem-64",
        "operating_system": "linux"
    },
    {
        "cores": 4,
        "memory": 26.0,
        "description": "4 core, 26GB Mem",
        "name": "n1-highmem-4",
        "operating_system": "linux"
    },
    {
        "cores": 32,
        "memory": 208.0,
        "description": "32 core, 208GB Mem",
        "name": "n1-highmem-32",
        "operating_system": "linux"
    }
]

WIN_INSTANCE_TYPES = [
    {
        "cores": 64,
        "memory": 416.0,
        "description": "64 core, 416GB Mem",
        "name": "n1-highmem-64-w",
        "operating_system": "windows"
    },
    {
        "cores": 4,
        "memory": 26.0,
        "description": "4 core, 26GB Mem",
        "name": "n1-highmem-4-w",
        "operating_system": "windows"
    },
    {
        "cores": 32,
        "memory": 208.0,
        "description": "32 core, 208GB Mem",
        "name": "n1-highmem-32-w",
        "operating_system": "windows"
    }
]

ALL_INSTANCE_TYPES = WIN_INSTANCE_TYPES+LIN_INSTANCE_TYPES

with open(os.path.join(os.path.dirname(__file__), "fixtures", "sw_packages.json"), 'r') as content:
    SOFTWARE = json.load(content)["data"]


class TestDataSingleton(unittest.TestCase):
 
    def setUp(self):
        projects_patcher = patch('ciocore.api_client.request_projects', return_value=PROJECTS)
        software_packages_patcher = patch('ciocore.api_client.request_software_packages', return_value=SOFTWARE)
        
        self.mock_projects = projects_patcher.start()
        self.mock_software_packages = software_packages_patcher.start()

        self.addCleanup(projects_patcher.stop)
        self.addCleanup(software_packages_patcher.stop)
        data.__data__ = {}
        data.__product__ = None

class TestDataAllInstanceTypes(TestDataSingleton):

    def setUp(self):
        super(TestDataAllInstanceTypes, self).setUp()
        instance_types_patcher = patch('ciocore.api_client.request_instance_types', return_value=ALL_INSTANCE_TYPES)
        self.mock_instance_types = instance_types_patcher.start()
        self.addCleanup(instance_types_patcher.stop)

    def test_init_sets_project_global(self):
        data.init("all")
        self.assertEqual(data.product(), "all") 

    def test_init_raises_if_product_falsy(self):
        with self.assertRaises(ValueError):
            data.init()
        with self.assertRaises(ValueError):
            data.init("")

    def test_data_raises_if_not_initialized(self):
        with self.assertRaises(ValueError):
            data.data()

    def test_valid(self):
        self.assertEqual(data.valid(), False) 
        data.init("all")
        data.data()
        self.assertEqual(data.valid(), True) 

    def test_clear(self):
        data.init("all")
        data.data()
        self.assertEqual(data.valid(), True) 
        data.clear()
        self.assertEqual(data.valid(), False) 

    def test_does_not_refresh_if_not_force(self):
        data.init("all")
        p1 = data.data()["projects"]
        self.assertEqual(len(p1), 4) 
        self.mock_projects.return_value =  ["a", "b"]
        p2 = data.data()["projects"]
        self.assertEqual(p2, p1) 

    def test_does_refresh_if_force_all(self):
        data.init("all")
        p1 = data.data()["projects"]
        self.assertEqual(len(p1), 4) 
        self.mock_projects.return_value =  ["a", "b"]
        p2 = data.data(force=True)["projects"]
        self.assertNotEqual(p2, p1) 
        self.assertEqual(len(p2), 2) 
        
    def test_get_data_for_one_product(self):
        data.init(product="cinema4d")
        inst = data.data()["instance_types"]
        sw = data.data()["software"]
        self.assertEqual(len(sw.supported_host_names()), 2) 

    def test_auto_filter_instance_types_based_on_software_plaforms(self):
        data.init(product="maya-io")
        inst = data.data()["instance_types"]
        self.assertEqual(len(inst), 4) 



class TestDataHomogenousInstanceTypes(TestDataSingleton):

    def setUp(self):
        super(TestDataHomogenousInstanceTypes, self).setUp()
        instance_types_patcher = patch('ciocore.api_client.request_instance_types', return_value=LIN_INSTANCE_TYPES)
        self.mock_instance_types = instance_types_patcher.start()
        self.addCleanup(instance_types_patcher.stop)

    def test_linux_only_instance_types(self):
        data.init(product="all")
        it = data.data()["instance_types"]
        self.assertEqual(len(it), 4) 

    def test_linux_only_packages_when_linux_only_instance_types(self):
        data.init(product="cinema4d")
        sw = data.data()["software"]
        print(sw.supported_host_names())
        self.assertEqual(len(sw.supported_host_names()), 1)

    def test_platforms_method_only_linux(self):
        data.init(product="cinema4d")
        data.data()
        self.assertEqual({"linux"}, data.platforms()) 
        


