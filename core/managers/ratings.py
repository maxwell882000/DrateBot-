"""
Module for manage ratings
"""
from revoratebot.models import Rating, User, Company
from django.db.models import Avg, Count
from Revorate import settings
import requests
import base64
import os


def create_rating(from_user: User, to_user: User, value: int) -> Rating:
    """
    Create a new rating from user to user
    :param from_user: from User
    :param to_user: to User
    :param value: estimate value
    :param comment: comment
    :return: created rating object
    """
    from_id = from_user.id
    to_id = to_user.id
    company_id = to_user.department.company_id
    department_id = to_user.department_id
    new_rating = Rating(to_id=to_id, from_id=from_id, value=value, company_id=company_id, department_id=department_id)
    new_rating.save()
    return new_rating


def set_comment_for_rating(rating_id: int, comment: str) -> Rating:
    """
    Set comment string for rating
    :param rating_id: Rating Id
    :param comment: Comment string
    :return: Rating
    """
    rating = get_rating_by_id(rating_id)
    rating.comment = comment
    rating.save()
    return rating


def _get_rating_screenshot_by_cloud_browser(company_id: int):
    key = settings.CLOUD_BROWSER_KEY
    host = settings.WEBHOOK_HOST
    url = 'https://api.cloudbrowser.co/v1/image?source=http://{host}/ratings/{company_id}/&key={key}&output_file_type=2&client_width=1366&client_height=768&capture_full_page=1'
    url = url.format(host=host, company_id=company_id, key=key)
    response = requests.get(url)
    json = response.json()
    image_string_base64 = json['base64']
    image_base64 = base64.decodestring(str.encode(image_string_base64))
    return image_base64


def get_img_ratings_for_company(company: Company):
    file_path = os.path.join(settings.BASE_DIR, 'static', 'media', 'ratings_{}.png'.format(company.id))
    image = _get_rating_screenshot_by_cloud_browser(company.id)
    with open(file_path, 'wb') as image_file:
        image_file.write(image)
    return file_path


def get_ratings_by_compnay(company_id: int):
    """
    Get users ratings in company
    :param company_id: Compnay Id
    :return: List of dictionaries with 'to_id' - user's id, 'avg_value' - avg user's estimate, 'count' - estimates' total count, ordered by avg value
    """
    return Rating.objects.values('to_id').filter(company_id=company_id).annotate(avg_value=Avg('value')).annotate(count=Count('value')).order_by('-avg_value')


def get_rating_by_id(rating_id: int) -> Rating:
    """
    Get rating by id
    :param rating_id: Rating id
    :return: Found rating
    """
    try:
        rating = Rating.objects.get(pk=rating_id)
    except Rating.DoesNotExists:
        return None
    return rating


def delete_users_ratings(user_id: int):
    """
    Delete all user's ratings
    :param user_id: User Id
    :return: void
    """
    ratings = Rating.objects.filter(to_id=user_id).delete()
