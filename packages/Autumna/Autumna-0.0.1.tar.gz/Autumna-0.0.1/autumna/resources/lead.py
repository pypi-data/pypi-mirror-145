import datetime
from enum import Enum

from .category import Category
from .service import Service

__all__ = ('Lead',)


class Lead:

    def __init__(
        self,
        id,
        category,
        service,
        to_email,
        from_email,
        date_time,
        content,
        enquirer_first_name,
        enquirer_surname,
        on_behalf_of,
        resident_first_name,
        resident_surname,
        telephone,
        is_anonymised,
        funding,
        timescales,
        instruction=None,
        visit_date=None,
        visit_time=None,
        email_permission=None,
        phone_permission=None,
        budget_type=None,
        budget_min=None,
        budget_max=None
    ):

        self.id = id
        self.category = category
        self.service = service
        self.to_email = to_email
        self.from_email = from_email
        self.date_time = date_time
        self.content = content
        self.enquirer_first_name = enquirer_first_name
        self.enquirer_surname = enquirer_surname
        self.on_behalf_of = on_behalf_of
        self.resident_first_name = resident_first_name
        self.resident_surname = resident_surname
        self.telephone = telephone
        self.is_anonymised = is_anonymised
        self.funding = funding
        self.timescales = timescales
        self.instruction = instruction
        self.visit_date = visit_date
        self.visit_time = visit_time
        self.email_permission = email_permission
        self.phone_permission = phone_permission
        self.budget_type = budget_type
        self.budget_min = budget_min
        self.budget_max = budget_max

    def __str__(self):
        return (
            f'[{self.category.name}] for {self.service.name}: '
            f'{self.enquirer_full_name} / {self.resident_full_name} '
            f'(#{self.id})'
        )

    @property
    def enquirer_full_name(self):
        parts = []

        if self.enquirer_first_name:
            parts.append(self.enquirer_first_name)

        if self.enquirer_surname:
            parts.append(self.enquirer_surname)

        return ' '.join(parts) or 'Name not given'

    @property
    def resident_full_name(self):
        parts = []

        if self.resident_first_name:
            parts.append(self.resident_first_name)

        if self.resident_surname:
            parts.append(self.resident_surname)

        return ' '.join(parts) or 'Name not given'

    @classmethod
    def from_json_type(cls, obj):

        date_time = datetime.datetime.strptime(
            obj['date'],
            '%Y-%m-%dT%H:%M:%S.%fZ'
        )

        category_specific_data = obj['categorySpecificData']

        return cls(
            obj['id'],
            Category.from_json_type(obj['category']),
            Service.from_json_type(obj['service']),
            obj['to'],
            obj['from'],
            date_time,
            obj['content'],
            obj['enquirerFirstName'],
            obj['enquirerSurname'],
            obj['onBehalfOf'],
            obj['residentFirstName'],
            obj['residentSurname'],
            obj['telephone'],
            obj['isAnonymised'],
            obj['funding'],
            obj['timescales'],
            instruction=category_specific_data.get('instruction'),
            visit_date=category_specific_data.get('visitDate'),
            visit_time=category_specific_data.get('visitTime'),
            email_permission=category_specific_data.get('emailPermission'),
            phone_permission=category_specific_data.get('phonePermission'),
            budget_type=category_specific_data.get('budgetType'),
            budget_min=category_specific_data.get('budgetMin'),
            budget_max=category_specific_data.get('budgetMax')
        )

    @classmethod
    def many(
        cls,
        api_client,
        date_from=None,
        date_to=None,
        is_anonymised=None,
        category_id=None,
        service_id=None
    ):

        params = {}

        if date_from is not None:
            params['dateFrom'] = date_from.strftime('%Y-%m-%d')

        if date_to is not None:
            params['dateTo'] = date_to.strftime('%Y-%m-%d')

        if is_anonymised is not None:
            params['isAnonymised'] = is_anonymised

        if category_id is not None:
            if isinstance(category_id, Enum):
                category_id = category_id.value
            params['categoryId'] = category_id

        if service_id is not None:
            params['serviceId'] = service_id

        objs = api_client('leads', params=params)

        return [cls.from_json_type(obj) for obj in objs]
