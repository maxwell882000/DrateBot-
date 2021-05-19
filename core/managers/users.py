from revoratebot.models import User, Department, Company
from typing import Optional, List
import secrets
from . import companies


def get_user_by_token(token: str) -> Optional[User]:
    """
    Get user by token
    :param token: token
    :return: User or None
    """
    try:
        user = User.objects.filter(token=token)[0]
    except IndexError:
        return None
    return user


def get_user_by_telegram_id(user_id: int) -> Optional[User]:
    """
    Get user by Telegram ID
    :param user_id: Telegram ID
    :return: User or None
    """
    try:
        user = User.objects.filter(telegram_user_id=user_id)[0]
    except IndexError:
        return None
    return user


def confirm_user(user: User, telegram_user_id):
    """
    Confirm user registration
    :param user: User
    :param telegram_user_id: User Telegram ID
    :return: If registration confirmed return True else return False
    """
    # If user registration already confirmed prevent access
    if user.confirmed:
        return False
    # If user is not a driver or a manager prevent access
    if not user.is_manager and not user.department.code_name == Department.DefaultNames.DRIVERS:
        return False
    # Confirm registration
    user.confirmed = True
    user.telegram_user_id = telegram_user_id
    user.save()
    return True


def set_user_language(user: User, language):
    """
    Set user language for Telegram Bot
    :param user: User
    :param language: language code, like 'ru', 'en' and 'uz'
    :return: void
    """
    user.language = language
    user.save()


def find_users_by_department_name(department_name: str, exclude_user_id: int, company_id: int) -> List[User]:
    """
    Find users by department name
    :param department_name: department name
    :param company_id: Current company id
    :return: list of users
    """
    return User.objects.filter(department__name=department_name, department__company_id=company_id).exclude(id=exclude_user_id)


def get_dispatchers() -> List[User]:
    """
    Get dispatchers
    :return: void
    """
    return User.objects.filter(department__code_name=Department.DefaultNames.DISPATCHERS)


def find_dispatcher_by_name(dispatcher_name: str) -> Optional[User]:
    """
    Find dispatcher by name
    :param dispatcher_name: Dispatcher name
    :return: Found dispatcher or None
    """
    try:
        dispatcher = User.objects.filter(department__code_name=Department.DefaultNames.DISPATCHERS, name=dispatcher_name)[0]
    except IndexError:
        dispatcher = None
    return dispatcher


def find_user_by_name(user_name: str) -> Optional[User]:
    """
    Find user by his name
    :param user_name: User name
    :return: User or None
    """
    try:
        return User.objects.filter(name=user_name)[0]
    except IndexError:
        return None


def get_registered_managers() -> List[User]:
    """
    Get registration confirmed managers
    :return: list of managers
    """
    return User.objects.filter(is_manager=True, confirmed=True)


def create_user(name: str, phone_number: str, company: str, department: str, is_manager: bool) -> User:
    """
    Create a new user with given data
    :param company: user company
    :param name: user name
    :param phone_number: user phone number
    :param department: user department
    :param is_manager: is user manager?
    :return: Cretaed user with him token
    """
    user_department = _get_new_edit_user_department(company, department, is_manager)
    token = secrets.token_urlsafe(20)
    user = User(name=name, phone_number=phone_number, department=user_department, token=token, is_manager=is_manager)
    user.save()
    return user


def get_by_id(user_id: int) -> Optional[User]:
    """
    Get user by id
    :param user_id: User id
    :return: Found user or None
    """
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return None
    return user


def _get_new_edit_user_department(company: str, department: str, is_manager: bool):
    if not is_manager:
        if not company.isdigit():
            # If user didn't select an exiting company, he wants to create a new one with given name
            user_company = companies.create_company(company)
            user_department = companies.create_department_for_company(department, user_company)
        else:
            company = int(company)
            user_company = companies.get_company_by_id(company)
            if not department.isdigit():
                # If user didn't select an exiting department in exiting company, he wants to create a new one
                user_department = companies.create_department_for_company(department, user_company)
            else:
                department = int(department)
                user_department = companies.get_department_by_id(department)
    else:
        user_department = None
    return user_department


def edit_user(user_id: int, name: str, phone_number: str, company: str, department: str, is_manager: bool) -> User:
    user = get_by_id(user_id)
    user.name = name
    user.phone_number = phone_number
    user.department = _get_new_edit_user_department(company, department, is_manager)
    user.is_manager = is_manager
    user.save()
    return user


def get_confirmed_users() -> List[User]:
    """
    Get confirmed non-managers
    :return: List of users
    """
    return User.objects.filter(confirmed=True, is_manager=False)
