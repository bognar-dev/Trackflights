from winotify import Notification, audio
from FlightRadar24.api import FlightRadar24API

# flightradar setup
fr_api = FlightRadar24API()

# winotify setup
toast = Notification(app_id="Look out the window!", title="")
toast.set_audio(audio.Default, loop=False)


class Flight:
clas