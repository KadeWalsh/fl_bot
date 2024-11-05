class DotDict:
    def __init__(self, data):
        print(f"DotDict input: {data.items()}")
        # print(*data.items(), sep = "\n\n")
        """Initialize the DotDict instance with a JSON dictionary."""
        self._data = {}
        for key, value in data.items():
            # If the value is a dictionary, recursively create another DotDict
            if isinstance(value, dict):
                self._data[key] = DotDict(value)
            else:
                self._data[key] = value

    def __getattr__(self, item):
        """Allow dot notation access to dictionary keys."""
        return self._data.get(item) or None
        try:
            return self._data[item]
        except KeyError:
            return None

    def __getitem__(self, item):
        """Allow bracket notation access."""
        return self._data[item]
        try:
            attr = self._data[item]
            print(attr)
            return attr
        except KeyError:
            print(f'Error!  Invalid Key: "{item}"')
            quit()

    def __setattr__(self, key, value):
        """Allow setting attributes using dot notation."""
        if key == "_data":
            super().__setattr__(key, value)
        else:
            self._data[key] = value

    def __setitem__(self, key, value):
        """Allow setting items using bracket notation."""
        self._data[key] = value

    def items(self):
        """Return the items of the dictionary."""
        return self._data.items()

    def keys(self):
        """Return the keys of the dictionary."""
        return self._data.keys()

    def values(self):
        """Return the values of the dictionary."""
        return self._data.values()

    def __len__(self):
        """Return the length of the dictionary."""
        return len(self._data)

    def __repr__(self):
        """String representation of the DotDict for easier debugging."""
        return f"DotDict({self._data})"
