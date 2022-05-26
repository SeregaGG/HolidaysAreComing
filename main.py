from Sender import Sender
from Settings.config import btx_webhook

btx_client = Sender(btx_webhook)
btx_client.start_send_tasks()
