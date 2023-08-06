""" test package_tree

   isort:skip_file
"""
import json
import os
import random
import sys
import unittest

from ciocore import package_tree
 
JSON_FILENAME = os.path.join(os.path.dirname(__file__) , "fixtures", "sw_packages.json")
with open(JSON_FILENAME, 'r') as content:
    packages_json = json.load(content)["data"]
 
SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)


class RemoveUnreachableTest(unittest.TestCase):

    def test_single_valid_tree_unchanged(self):
        paths = ["a", "a/b", "a/b/c"]
        results = package_tree.remove_unreachable(paths)
        self.assertEqual(results, paths)

    def test_many_valid_trees_unchanged(self):
        paths = ["a", "a/b", "a/b/c", "b", "b/b", "b/b/c", "c", "c/b", "c/b/c"]
        results = package_tree.remove_unreachable(paths)
        self.assertEqual(results, paths)

    def test_single_invalid_tree_culled_leaf(self):
        paths = ["a", "a/b", "b/b/c"]
        results = package_tree.remove_unreachable(paths)
        self.assertEqual(results, ["a", "a/b"])

    def test_single_invalid_tree_culled_below(self):
        paths = ["a", "b/b", "a/b/c"]
        results = package_tree.remove_unreachable(paths)
        self.assertEqual(results, ["a"])

    def test_multiple_invalid_tree_culled(self):
        paths = ["a", "a/b", "a/b/c", "b", "b/b", "b/b/c", "d", "c/b", "c/b/c"]
        results = package_tree.remove_unreachable(paths)
        self.assertEqual(
            results, [
                "a", "a/b", "a/b/c", "b", "b/b", "b/b/c", "d"])

    def test_random_input_order(self):
        paths = ["a", "a/b", "a/b/c", "b", "b/b", "b/b/c", "d", "c/b", "c/b/c"]
        random.shuffle(paths)
        results = package_tree.remove_unreachable(paths)
        self.assertEqual(
            results, [
                "a", "a/b", "a/b/c", "b", "b/b", "b/b/c", "d"])


class ToNameTest(unittest.TestCase):

    def test_major_only(self):
        pkg = {
            "product": "foo-bar",
            "major_version": "1",
            "minor_version": "",
            "release_version": "",
            "build_version": ""
        }
        expected = "foo-bar 1"
        self.assertEqual(package_tree.to_name(pkg), expected)

    def test_major_minor(self):
        pkg = {
            "product": "foo-bar",
            "major_version": "1",
            "minor_version": "3",
            "release_version": "",
            "build_version": ""
        }
        expected = "foo-bar 1.3"
        self.assertEqual(package_tree.to_name(pkg), expected)

    def test_major_minor_release(self):
        pkg = {
            "product": "foo-bar",
            "major_version": "1",
            "minor_version": "3",
            "release_version": "62",
            "build_version": ""
        }
        expected = "foo-bar 1.3.62"
        self.assertEqual(package_tree.to_name(pkg), expected)

    def test_major_minor_release_build(self):
        pkg = {
            "product": "foo-bar",
            "major_version": "1",
            "minor_version": "3",
            "release_version": "62",
            "build_version": "876"
        }
        expected = "foo-bar 1.3.62.876"
        self.assertEqual(package_tree.to_name(pkg), expected)

    def test_platform(self):
        pkg = {
            "product": "foo-bar",
            "major_version": "1",
            "minor_version": "",
            "release_version": "",
            "build_version": "",
            "platform": "windows"
        }
        expected = "foo-bar 1 windows"
        self.assertEqual(package_tree.to_name(pkg), expected)


class SoftwareDataInitTest(unittest.TestCase):

    def test_smoke(self):
        pt = package_tree.PackageTree([])
        self.assertIsInstance(pt, package_tree.PackageTree)

    def test_init_with_product(self):
        pt = package_tree.PackageTree(packages_json, product="houdini")
        self.assertEqual(len(pt.tree["children"]), 2)
        pt = package_tree.PackageTree(packages_json, product="maya-io")
        self.assertEqual(len(pt.tree["children"]), 9)

    def test_init_with_no_product(self):
        pt = package_tree.PackageTree(packages_json)
        self.assertEqual(len(pt.tree["children"]), 79)

    def test_init_with_sub_product(self):
        pt = package_tree.PackageTree(
            packages_json,
            product="arnold-houdini")
        self.assertEqual(len(pt.tree["children"]), 4)

    def test_init_with_windows_product(self):
        pt = package_tree.PackageTree(
            packages_json,
            product="cinema4d")
        self.assertEqual(len(pt.tree["children"]), 2)

class SoftwareDataTestInitPlatformFilter(unittest.TestCase):

    def test_does_not_filter_by_default(self):
        pt = package_tree.PackageTree(packages_json, product="cinema4d")
        self.assertEqual(len(pt.tree["children"]), 2)
  
    def test_filter_windows(self):
        pt = package_tree.PackageTree(packages_json, product="cinema4d", platforms=["windows"])
        self.assertEqual(len(pt.tree["children"]), 1)
        self.assertEqual(pt.tree["children"][0]["platform"], "windows")
        
    def test_filter_linux(self):
        pt = package_tree.PackageTree(packages_json, product="cinema4d", platforms=["linux"])
        self.assertEqual(len(pt.tree["children"]), 1)
        self.assertEqual(pt.tree["children"][0]["platform"], "linux")
        
    def test_raise_bad_platform(self):
        with self.assertRaises(KeyError):
            pt = package_tree.PackageTree(packages_json, product="cinema4d", platforms=["bad"])
 

class SoftwareDataFindByKeysTest(unittest.TestCase):

    def setUp(self):
        self.pt = package_tree.PackageTree(packages_json, product="houdini")

    def test_find_host_by_keys(self):
        keys = {
            'product': 'houdini',
            'major_version': '16',
            'minor_version': '5',
            'release_version': '323',
            'build_version': '',
            'plugin_host_product': '',
            'plugin_host_version': ''
        }
        pkg = self.pt.find_by_keys(**keys)
        self.assertEqual(pkg["product"], 'houdini')
        self.assertEqual(pkg["major_version"], '16')
        self.assertEqual(pkg["minor_version"], '5')
        self.assertEqual(pkg["release_version"], '323')

    def test_find_leaf_by_keys(self):
        keys = {
            'product': 'al-shaders',
            'major_version': '1',
            'minor_version': '1',
            'release_version': '',
            'build_version': '',
            'plugin_host_product': '',
            'plugin_host_version': ''
        }
        pkg = self.pt.find_by_keys(**keys)
        self.assertEqual(pkg["product"], 'al-shaders')
        self.assertEqual(pkg["major_version"], '1')
        self.assertEqual(pkg["minor_version"], '1')

    def test_find_nonexistent_package_returns_none(self):
        keys = {
            'product': 'arnold-houdini',
            'major_version': '7',
            'minor_version': '1',
            'release_version': '',
            'build_version': '',
            'plugin_host_product': '',
            'plugin_host_version': ''
        }
        pkg = self.pt.find_by_keys(**keys)
        self.assertEqual(pkg, None)


class SoftwareDataFindByPathTest(unittest.TestCase):

    def setUp(self):
        self.pt = package_tree.PackageTree(packages_json, product="houdini")

    def test_find_root_path(self):
        path = "houdini 16.0.736 linux"
        pkg = self.pt.find_by_path(path)
        self.assertEqual(package_tree.to_name(pkg), path)

    def test_find_leaf_path(self):
        path = "houdini 16.0.736 linux/arnold-houdini 2.0.2.2 linux/al-shaders 1.0 linux"
        pkg = self.pt.find_by_path(path)
        self.assertEqual(package_tree.to_name(pkg), "al-shaders 1.0 linux")

    def test_find_nonexistent_path_return_none(self):
        path = "houdini 16.0.736 linux/arnold-houdini 9.0.2.2 linux"
        pkg = self.pt.find_by_path(path)
        self.assertEqual(pkg, None)

    def test_find_empty_path_return_none(self):
        path = ""
        pkg = self.pt.find_by_path(path)
        self.assertEqual(pkg, None)

    def test_find_none_path_return_none(self):
        path = None
        pkg = self.pt.find_by_path(path)
        self.assertEqual(pkg, None)

class FindByNameTest(unittest.TestCase):
    def setUp(self):
        self.pt = package_tree.PackageTree(packages_json, product="houdini")

    def test_find_root(self):
        name = 'houdini 16.5.323 linux'
        result = self.pt.find_by_name(name)
        self.assertEqual(package_tree.to_name(result), name)

    def test_find_root_when_limit_1(self):
        name = 'houdini 16.5.323 linux'
        result = self.pt.find_by_name(name, 1)
        self.assertEqual(package_tree.to_name(result), name)

    def test_find_plugin_level(self):
        name = "arnold-houdini 2.0.2.2 linux"
        result = self.pt.find_by_name(name)
        self.assertEqual(package_tree.to_name(result), name)

    def test_find_plugin_level_high_limit(self):
        name = "arnold-houdini 2.0.2.2 linux"
        result = self.pt.find_by_name(name, 2)
        self.assertEqual(package_tree.to_name(result), name)

    def test_dont_find_plugin_level_when_limited(self):
        name = "arnold-houdini 2.0.2.2 linux"
        result = self.pt.find_by_name(name, 1)
        self.assertEqual(result, None)


class SoftwareDataGetAllPathsTest(unittest.TestCase):

    def setUp(self):
        self.pt = package_tree.PackageTree(packages_json, product="houdini")

    def test_get_all_paths_to_root(self):

        keys = {
            'product': 'houdini',
            'major_version': '16',
            'minor_version': '5',
            'release_version': '323',
            'build_version': '',
            'plugin_host_product': '',
            'plugin_host_version': '',
            'platform': 'linux',
            
        }
        paths = self.pt.get_all_paths_to(**keys)
        self.assertTrue(
            'houdini 16.5.323 linux' in paths)
        self.assertEqual(len(paths), 1)

    def test_get_all_paths_to_leaf(self):

        keys = {
            'product': 'al-shaders',
            'major_version': '1',
            'minor_version': '0',
            'release_version': '',
            'build_version': '',
            'plugin_host_product': '',
            'plugin_host_version': '',
            "platform": "linux"
        }
        paths = self.pt.get_all_paths_to(**keys)
        self.assertTrue(
            'houdini 16.0.736 linux/arnold-houdini 2.0.1 linux/al-shaders 1.0 linux' in paths)
        self.assertEqual(len(paths), 2)

    def test_get_all_paths_to_nonexistent(self):

        keys = {
            'product': 'foo',
            'major_version': '1',
            'minor_version': '0',
            'release_version': '',
            'build_version': '',
            'plugin_host_product': '',
            'plugin_host_version': '',
            "platform": "linux"
        }
        paths = self.pt.get_all_paths_to(**keys)
        self.assertEqual(paths, [])


class SoftwarePlatformsSetTest(unittest.TestCase):
    # There are Windows packages in c4d but not Maya.
    def test_only_linux(self):
        pt = package_tree.PackageTree(packages_json, product="maya-io")
        self.assertEqual({"linux"}, pt.platforms())
        
    def test_linux_and_windows(self):
        pt = package_tree.PackageTree(packages_json, product="cinema4d")
        self.assertEqual({"windows", "linux"}, pt.platforms())
        

class SupportedHostNamesTest(unittest.TestCase):
    def setUp(self):
        self.pt = package_tree.PackageTree(packages_json, product="maya-io")
        self.one_hostname = 'maya-io 2018.SP2 linux'

    def test_supported_host_names(self):

        host_names = self.pt.supported_host_names()

        self.assertEqual(len(host_names), 9)
        self.assertIn(self.one_hostname, host_names)

    def test_supported_host_names_windows(self):
        self.pt = package_tree.PackageTree(packages_json, product="cinema4d")
        host_names = self.pt.supported_host_names()
        self.assertEqual(len(host_names), 2)
        self.assertIn('cinema4d 25.117.RB316423 windows', host_names)


class SupportedPluginsTest(unittest.TestCase):
    def setUp(self):
        self.pt = package_tree.PackageTree(packages_json, product="maya-io")
        self.one_hostname = 'maya-io 2018.SP2 linux'

    def test_supported_plugins_count(self):
        plugins = self.pt.supported_plugins(self.one_hostname)
        self.assertEqual(len(plugins), 4)

    
    def test_supported_plugins_keys(self):
        plugins = self.pt.supported_plugins(self.one_hostname)
        self.assertIsInstance(plugins[0], dict)
        self.assertIn("plugin",plugins[0])
        self.assertIn("versions",plugins[0])

    def test_supported_plugins_version_count(self):
        plugins = self.pt.supported_plugins(self.one_hostname)
        self.assertEqual(len(plugins[0]["versions"]), 8)

# TODO Test PackageTree#get_environment()


if __name__ == '__main__':
    unittest.main()
