from django.db.models import get_models, get_app
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered

def autoregisterm(*app_list):
    for app_name in app_list:
        app_models = get_app(app_name)
        for model in get_models(app_models):
            try:
                admin.site.register(model)
            except AlreadyRegistered:
                pass
def autoregister(apps):
    for app in apps:
        # exclude django apps
        if not app.startswith('django.'):
            try:
                autoregisterm(app)
            except:
                pass