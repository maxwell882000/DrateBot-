from revoratebot.models import Company, Department
from typing import Optional, List


def create_default_company_departments(company: Company):
    """
    Create default departments for new company
    :param company: New company
    :return: void
    """
    dispatchers = Department(name='Dispatchers', company=company, code_name=Department.DefaultNames.DISPATCHERS)
    dispatchers.save()
    drivers = Department(name='Drivers', code_name=Department.DefaultNames.DRIVERS, company=company)
    drivers.save()
    updaters = Department(name='Update', company=company)
    updaters.save()
    safety = Department(name='Safety', company=company)
    safety.save()
    fleet = Department(name='Fleet', company=company)
    fleet.save()
    trailer = Department(name='Trailer', company=company)
    trailer.save()
    logbook = Department(name='Logbook', company=company)
    logbook.save()


def get_company_by_id(company_id) -> Optional[Company]:
    """
    Get company instance by id
    :param company_id: Company Id
    :return: Found company or None
    """
    try:
        company = Company.objects.get(pk=company_id)
    except Company.DoesNotExist:
        return None
    return company


def create_company(name: str) -> Company:
    """
    Create a new company
    :param name: company name
    :return: instance of new company
    """
    company = Company(name=name)
    company.save()
    create_default_company_departments(company)
    return company


def create_department_for_company(department_name: str, company: Company) -> Department:
    """
    Create department in company
    :param department_name: Department name
    :param company: Company
    :return: instance of new department
    """
    department = Department(name=department_name, company=company)
    department.save()
    return department


def get_department_by_id(department_id: int) -> Optional[Department]:
    """
    Get department by id
    :param department_id: Department Id
    :return: Found department or None
    """
    try:
        department = Department.objects.get(pk=department_id)
    except Department.DoesNotExist:
        return None
    return department


def get_all_companies() -> List[Company]:
    """
    Get all companies
    :return: List of companies
    """
    return Company.objects.all()


def get_all_departments() -> List[Department]:
    """
    Get all departments
    :return: List of departments
    """
    return Department.objects.all()


def get_company_by_name(name: str) -> Optional[Company]:
    try:
        company = Company.objects.filter(name=name)[0]
    except IndexError:
        return None
    return company


def get_company_users_counts(company_id: int):
    company = get_company_by_id(company_id)
    departments = company.department_set.all()
    users_count = 0
    confirmed_users_count = 0
    non_confirmed_users_count = 0
    for department in departments:
        department_users = department.user_set.all()
        users_count += department.user_set.count()
        confirmed_users_count += department.user_set.filter(confirmed=True).count()
        non_confirmed_users_count += department.user_set.filter(confirmed=False).count()
    return users_count, confirmed_users_count, non_confirmed_users_count
