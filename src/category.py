import os

from .achievement import Achievement, AchievementDuration, AchievementTime
from .mixins import JsonMixin, SlugMixin

class InvalidAchievementException(Exception):
    pass

class InvalidCategoryException(Exception):
    pass

class InvalidCategoryTypeException(Exception):
    pass

class Category(JsonMixin, SlugMixin):
    TYPES = [
        'timeline',
        'box',
        'card',
        'list',
        'nested',
        'optional',
    ]

    def __init__(self, name, type=None, items=None):
        self.name = name
        self.type = type or 'box'
        self.items = items or []

        if self.type not in Category.TYPES:
            raise InvalidCategoryTypeException(self.type)

        super().__init__()

    def _serialize(self):
        obj = {}
        obj['items'] = self.items
        self.items = [item.slug for item in obj['items']]
        return obj

    def _validate(self):
        for item in self.items:
            if self.type == 'nested':
                if not isinstance(item, Category) or item.type != 'list':
                    raise InvalidCategoryException(item)

            if self.type != 'nested' and not isinstance(item, Achievement):
                raise InvalidAchievementException(item)

    def new_subcategory(self, **args):
        if self.type != 'nested':
            raise InvalidCategoryTypeException('Category must be of nested type.')
        category = Category(**args)
        self.items.append(category)
        return category

    def _new_achievement(self, T, **args):
        if self.type == 'nested':
            raise InvalidCategoryTypeException('Category must not be nested type.')
        achievement = T(**args)
        self.items.append(achievement)
        self.items.sort(reverse=True)
        return achievement

    def new_achievement_duration(self, **args):
        return self._new_achievement(AchievementDuration, **args)

    def new_achievement_time(self, **args):
        return self._new_achievement(AchievementTime, **args)

    def to_json(self, dir_path=None):
        dir_path = dir_path or os.path.join('assets', self.slug)

        self._validate()

        for item in self.items:
            path = os.path.join(dir_path, item.slug) if self.type == 'nested' else os.path.join(dir_path, '{}.json'.format(item.slug))

            item.to_json(path)

        super().to_json(os.path.join(dir_path, '{}.json'.format(self.slug)))
