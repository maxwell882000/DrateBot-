from revoratebot.models import Rating
from core.managers import users
from typing import List, Dict


class RatingViewModel:
    def __init__(self, rating: Rating):
        self.id = rating.id
        self.from_user = users.get_by_id(rating.from_id)
        self.to_user = users.get_by_id(rating.to_id)
        self.value = rating.value
        self.created_at = rating.created_at
        self.comment = rating.comment


class CompanyRatingViewModel:
    def __init__(self, rating: Dict):
        self.user = users.get_by_id(rating['to_id'])
        self.avg_value = rating['avg_value']
        self.count = rating['count']
