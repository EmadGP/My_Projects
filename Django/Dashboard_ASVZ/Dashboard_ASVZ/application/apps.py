# application/apps.py
from django.apps import AppConfig
import threading

class ApplicationConfig(AppConfig):
    name = 'application'

    def ready(self):
        # Start the MQTT listener in a separate thread
        mqtt_thread = threading.Thread(target=self.start_mqtt_listener)
        mqtt_thread.daemon = True  # Ensures the thread exits with the server
        mqtt_thread.start()

    def start_mqtt_listener(self):
        # Delay importing `MqttService` until Django is fully loaded
        from .mqtt_service import MqttService

        # Initialize and start the MQTT listener
        mqtt_service = MqttService()
        mqtt_service.listen()
