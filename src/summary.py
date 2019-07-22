import datetime as dt
import os

from .basic import Basic
from .category import Category
from .mixins import JsonMixin, SlugMixin

class InvalidBasicException(Exception):
    pass

class InvalidCategoryException(Exception):
    pass

class Summary(JsonMixin, SlugMixin):
    DATETIME_FORMAT = '%B %d, %Y'

    def __init__(
        self,
        name,
        title,
        email,
        phone,
        introduction,
        links=None,
        categories=None
    ):
        self.name = name
        self.title = title
        self.email = email
        self.phone = phone
        self.introduction = introduction
        self.links = links or {}
        self.categories = categories or []
        self.updated = dt.datetime.now().strftime(Summary.DATETIME_FORMAT)

        super().__init__()


    def _validate(self):
        for category in self.categories:
            if not isinstance(category, Category):
                raise InvalidCategoryException(category)

    def new_category(self, **args):
        category = Category(**args)
        self.categories.append(category)
        return category

    def _serialize(self):
        obj = {'categories': self.categories}
        self.categories = [category.slug for category in self.categories]
        return obj

    def to_json(self, dir_path=None):

        dir_path = dir_path or 'assets'
        path = os.path.join(dir_path, '{}.json'.format(self.slug))
        os.makedirs(dir_path, exist_ok=True)

        self._validate()

        super().to_json(path)
        for category in self.categories:
            path = os.path.join(dir_path, category.slug)
            category.to_json(path)
