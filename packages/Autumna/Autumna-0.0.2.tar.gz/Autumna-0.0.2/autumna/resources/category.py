
__all__ = ('Category')


class Category:
    """
    Leads come in different categories, each category of lead has it's own
    set of specific fields.
    """

    def __init__(self, id, name):

        self.id = id
        self.name = name

    def __str__(self):
        return f'{self.name} (#{self.id})'

    @classmethod
    def from_json_type(cls, obj):
        return cls(obj['id'], obj['name'])
