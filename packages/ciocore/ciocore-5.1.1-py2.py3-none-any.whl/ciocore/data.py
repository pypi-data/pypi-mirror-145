# Everything from the endpoints.


"""
Data from Conductor endpoints as a singleton.

Also has the ability to use fixtures for dev purposes. 

TODO: Develop fixture functionality to serve as a local cache, possibly for air_gapped studio
workstations. 
"""
import json
import os
from ciocore.package_tree import PackageTree
from ciocore import api_client

__data__ = {}
__product__ = None
__fixtures_dir__ = None
__platforms__ = None

def data(force=False):
    """
    Get projects , instance_types, and software from fixtures or api.

    Data will be valid.

    args: force

    """

    global __data__
    global __product__
    global __fixtures_dir__
    global __platforms__


    if not __product__:
        raise ValueError(
            'Data must be initialized before use, e.g. data.init("maya-io") or data.init("all").'
        )

    if force:
        clear()

    if __data__ == {}:
        # PROJECTS
        projects_json = _get_json_fixture("projects")
        if projects_json:
            __data__["projects"] = projects_json
        else:
            __data__["projects"] = sorted(api_client.request_projects())

        # INST_TYPES
        instance_types = _get_json_fixture("instance_types")
        if not instance_types:
            instance_types = api_client.request_instance_types()

        it_platforms = set([it["operating_system"] for it in instance_types])

        # SOFTWARE
        software = _get_json_fixture("software")
        if not software:
            software = api_client.request_software_packages()

        kwargs = {"platforms":it_platforms}
        if not  __product__ == "all":
            kwargs["product"] = __product__

        software_tree = PackageTree(software, **kwargs)

        if software_tree.tree:
            __data__["software"] = software_tree
            # Revisit instance types to filter out any that are not needed for any software package.
            sw_platforms = software_tree.platforms()
            instance_types = [it for it in instance_types if it["operating_system"] in sw_platforms]
        
        __data__["instance_types"] = sorted(instance_types, key=lambda k: (k["cores"], k["memory"]))
        __platforms__ = set([it["operating_system"] for it in __data__["instance_types"]])
    
    return __data__


def valid():
    global __data__
    if not __data__.get("projects"):
        return False
    if not __data__.get("instance_types"):
        return False
    if not __data__.get("software"):
        return False
    return True


def clear():
    global __data__
    __data__ = {}


def init(product=None):
    global __product__
    if not product:
        raise ValueError("You must specify a product or 'all'")
    __product__ = product


def product():
    global __product__
    return __product__


def set_fixtures_dir(rhs):
    global __fixtures_dir__
    __fixtures_dir__ = rhs or ""


def _get_json_fixture(resource):
    global __fixtures_dir__
    if __fixtures_dir__:
        cache_path = os.path.join(__fixtures_dir__, "{}.json".format(resource))
        if os.path.isfile(cache_path):
            try:
                with open(cache_path) as f:
                    return json.load(f)
            except BaseException:
                pass

def platforms():
    """
    The set of platforms that satisfy both software and instance types.
    
    It's updated whenever data() is updated.
    """
    global __platforms__
    return __platforms__