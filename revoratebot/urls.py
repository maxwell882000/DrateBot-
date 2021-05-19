from django.urls import path
from .views import index, companies, departments, users, ratings, sos, bot
from Revorate.settings import WEBHOOK_URL_PATH

urlpatterns = [
    path('', index.IndexView.as_view(), name='admin_home'),
    path('companies/', companies.CompaniesListView.as_view(), name='admin_companies_list'),
    path('companies/<int:pk>', companies.CompanyView.as_view(), name='admin_company'),
    path('companies/create', companies.CreateCompanyView.as_view(), name='admin_new_company'),
    path('companies/<int:pk>/delete', companies.DeleteCompanyView.as_view(), name='admin_delete_company'),
    path('companies/<int:pk>/edit', companies.UpdateCompanyView.as_view(), name='admin_edit_company'),
    path('companies/<int:company_id>/departments/create', departments.CreateDepartmentView.as_view(), name='admin_new_department'),
    path('companies/<int:company_id>/departments/<int:pk>', departments.EditDepartmentView.as_view(), name='admin_edit_department'),
    path('companies/<int:company_id>/departments/<int:pk>/delete', departments.DeleteDepartmentView.as_view(), name='admin_delete_department'),
    path('users/', users.UsersListView.as_view(), name='admin_users'),
    path('users/new', users.CreateUserView.as_view(), name='admin_new_user'),
    path('users/<int:pk>/created', users.UserCreatedView.as_view(), name='admin_user_created'),
    path('users/<int:pk>', users.EditUserView.as_view(), name='admin_edit_user'),
    path('users/<int:pk>/delete', users.DeleteUserView.as_view(), name='admin_delete_user'),
    path('ratings/', ratings.RatingsListView.as_view(), name='admin_ratings'),
    path('ratings/<int:pk>/edit/', ratings.EditRatingView.as_view(), name='admin_edit_rating'),
    path('ratings/<int:company_id>/', ratings.BotCompanyRatingView.as_view(), name='bot_company_ratings'),
    path('sos/', sos.SosSignalsListView.as_view(), name='admin_sos'),
    path('init/', bot.BotInitializeView.as_view()),
    path('bot/' + WEBHOOK_URL_PATH, bot.BotUpdatesRecieverView.as_view())
]
