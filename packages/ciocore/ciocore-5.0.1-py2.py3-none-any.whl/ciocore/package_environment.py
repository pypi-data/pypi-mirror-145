class PackageEnvironment(object):
    """Encapsulate the submission environment vars.

    Handle building up the env with a single call to extend()
    """

    def __init__(self, env_list=None, platform=None):
        """Initialize, possibly with a package or list of variables.

        On the first add, if the package contains a platform field (which it will) or in the case of a list, it is
        accompanied by a platform, then we use it, otherwise we default to linux. It is an error to
        try to change platform after the first add.

        The merge policy is effectively set the first time a variable is declared and used for all
        subsequent amendments. Policy is implied by the storage data type. String=exclusive,
        List=append. User cannot change the policy once a variable has been declared.

        """
        self.platform = None
        self._env = {}
        # delegete all initialization to extend()
        self.extend(env_list, platform)

    def _set(self, name, value):
        """Set the value of an exclusive variable.

        Can be overwritten by subsequent adds.

        It is an error if the variable has already been declared with policy=append.
        """
        if self._env.get(name) and isinstance(self._env[name], list):
            raise ValueError(
                "Can't change merge policy for '{}' from 'append' to 'exclusive'.".format(name)
            )
        self._env[name] = value

    def _append(self, name, value):
        """Set the value of an append variable.

        Can be appended to with subsequent adds.

        It is an error if the variable has already been declared with policy=exclusive.
        """
        if self._env.get(name):
            if not isinstance(self._env[name], list):
                raise ValueError(
                    "Can't change merge policy for '{}' from 'exclusive' to 'append'.".format(name)
                )
        else:
            self._env[name] = []
        self._env[name].append(value)

    def extend(self, env_list, platform=None):
        """Extend with the given variable specifications.

        env_list is either:
        A list of objects OR an object with an "environment" key that contains a
        list of objects. The latter is the structure of a package. Therefore we can initialize or extend
        a PackageEnvironment with a package.

        Each of these objects in the list has a name, a value, and a merge_policy. One by one
        they are added according to their merge policy. See _set and _append above.
        """

        if not env_list:
            return

        try:
            others = env_list["environment"]
            requested_platform = env_list.get("platform")
        except TypeError:
            others = env_list
            requested_platform = platform

        if not self.platform:
            self.platform = requested_platform or "linux"
        elif requested_platform and requested_platform != self.platform:
            raise ValueError("Can't change platform once initialized.")

        for var in others:
            name = var["name"]
            value = var["value"]
            policy = var["merge_policy"]
            if policy not in ["append", "exclusive"]:
                raise ValueError("Unexpected merge policy: %s" % policy)

            if policy == "append":
                self._append(name, value)
            else:
                self._set(name, value)

    def __iter__(self):
        """Cast the object as a dict."""
        sep = ";" if self.platform == "windows" else ":"
        for key in self._env:
            var = self._env[key]
            if isinstance(var, list):
                yield key, sep.join(var)
            else:
                yield key, var

    def __getitem__(self, key):
        """Allow access by key."""
        sep = ";" if self.platform == "windows" else ":"
        var = self._env.__getitem__(key)
        if isinstance(var, list):
            return sep.join(var)
        return var
