import os

from .mixins import JsonMixin, SlugMixin

class Basic(JsonMixin, SlugMixin):
    def __init__(self, name, email, phone, introduction, links=None):
        self.name = name
        self.email = email
        self.phone = phone
        self.introduction = introduction
        self.links = links or {}

        super().__init__()


    def to_json(self, dir_path=None):
        dir_path = dir_path or 'assets'
        path = os.path.join(dir_path, '{}.json'.format(self.slug))

        super().to_json(path)
