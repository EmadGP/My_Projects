from django.core.management.base import BaseCommand
from application.mqtt_service import MqttService

class Command(BaseCommand):
    help = 'Luister naar MQTT-berichten en werk de snooze tijden bij'

    def handle(self, *args, **kwargs):
        mqtt_service = MqttService()
        mqtt_service.listen()
