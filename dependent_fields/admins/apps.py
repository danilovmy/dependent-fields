from django.contrib.admin.apps import AdminConfig as BaseAdminConfig


class AdminsConfig(BaseAdminConfig):
    default_site = 'admins.admin.AdminSite'
    label = 'admin'
