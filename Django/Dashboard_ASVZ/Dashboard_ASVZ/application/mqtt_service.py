import logging
import time
from datetime import datetime
from paho.mqtt import client as mqtt_client
from .models import Pump
from django.utils.timezone import make_aware

# Configuratie voor de MQTT broker
BROKER = 'asvz.local'
PORT = 1883
TOPIC = 'available_devices'
USERNAME = 'asvz'
PASSWORD = 'asvz'

# Logger instellen
logger = logging.getLogger(__name__)


class MqttService:
    def __init__(self):
        # Verwijder callback_api_version
        self.client = mqtt_client.Client('mqtt-subscriber')
        self.client.username_pw_set(USERNAME, PASSWORD)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def connect(self):
        """Verbind met de MQTT broker."""
        try:
            self.client.connect(BROKER, PORT)
            logger.info("Verbonden met MQTT broker.")
        except Exception as e:
            logger.error(f"Kon niet verbinden met MQTT broker: {e}")
            raise

    def on_connect(self, client, userdata, flags, rc):
        """Callback voor succesvolle verbinding."""
        if rc == 0:
            logger.info("Succesvol verbonden met MQTT broker.")
            client.subscribe(TOPIC)
        else:
            logger.error(f"Verbinding mislukt, return code {rc}")

    def on_message(self, client, userdata, msg):
        """Callback voor ontvangen berichten."""
        message = msg.payload.decode()
        pump_id = self.extract_pump_id(message)

        if pump_id:
            try:
                pump = Pump.objects.get(id=pump_id)
                pump.last_snoozed = make_aware(datetime.now())
                pump.save()
                logger.info(f"Snooze tijd bijgewerkt voor Pump {pump_id}")
            except Pump.DoesNotExist:
                logger.error(f"Pomp met ID {pump_id} bestaat niet.")

    def extract_pump_id(self, message):
        """Haalt de pomp ID uit het bericht, veronderstellende formaat 'Pump X activated'."""
        try:
            # Voorbeeld bericht: "Pump 1 activated"
            return int(message.split()[1])
        except (IndexError, ValueError):
            logger.error(f"Kon pomp ID niet extraheren uit bericht: {message}")
            return None

    def listen(self):
        """Begin met luisteren naar berichten."""
        self.connect()
        self.client.loop_start()
        while True:
            time.sleep(1)  # Voorkom hoge CPU-belasting
