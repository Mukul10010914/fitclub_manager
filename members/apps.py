from django.apps import AppConfig


class MembersConfig(AppConfig):
    name = 'members'

    def ready(self):
    	from subscription_updater import updater
    	updater.start()
