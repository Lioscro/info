import json
import os
import pandas as pd

class SlugMixin:
    REPLACE_DICT = {
        ' ': '_',
        '/': '_',
        '(': '',
        ')': '',
        '.': ''
    }

    def __init__(self):
        self.slug = self.replace_all(self.name, SlugMixin.REPLACE_DICT).lower()

    def replace_all(self, s, replace_dict):
        for key, item in replace_dict.items():
            s = s.replace(key, item)
        return s

class JsonMixin:
    def _serialize(self):
        return {}

    def _deserialize(self, obj):
        for key, item in obj.items():
            setattr(self, key, item)

    def to_json(self, path):
        # Make parent directory.
        dirname = os.path.dirname(path)
        os.makedirs(dirname, exist_ok=True)

        obj = self._serialize()
        with open(path, 'w') as f:
            json.dump(
                self,
                f,
                ensure_ascii=False,
                default=lambda obj: obj.__dict__,
                indent=4,
            )
        self._deserialize(obj)
