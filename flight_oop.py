from winotify import Notification, audio
from FlightRadar24.api import FlightRadar24API

# flightradar setup
fr_api = FlightRadar24API()


class AirplanesInfrontWindow:

    def __init__(self):
        self.flights = []
        self.previous_flights = []
        self.sunny = False
        self.area_infront_window = {}
        self.task_done = False

        # winotify setup
        self.toast = Notification(app_id="Look out the window!", title="")
        self.toast.set_audio(audio.Reminder, loop=False)

    def set_weather(self) -> bool:
        self.sunny = int(input("Please Choose your weather.\n(1) Sunny (0) Cloudy\n"))
        return bool(self.sunny)

    def list_of_flights_in_area(self):
        if self.sunny:
            self.area_infront_window = {'tl_y': 51.186454, 'tl_x': 6.363371, 'br_y': 51.102381, 'br_x': 6.578291}
        if not self.sunny:
            self.area_infront_window = {'tl_y': 51.186454, 'tl_x': 6.363371, 'br_y': 51.102381, 'br_x': 6.578291}
        bounds_mgl = fr_api.get_bounds(self.area_infront_window)
        self.flights = fr_api.get_flights(bounds=bounds_mgl)
        if not self.sunny:
            for flight in self.flights:
                if flight.altitude >= 7000:
                    self.flights.remove(flight)

        return self.flights

    def new_flight_in_area(self) -> bool:
        if len(self.flights) > len(self.previous_flights):
            return True
        else:
            self.previous_flights = self.flights
            return self.new_flight_in_area()

    def print_flights(self):
        TWENTY_MINS_IN_SEC = 1200
        print("New flight")
        flight = self.flights[-1]
        details = fr_api.get_flight_details(flight_id=flight.id)
        try:
            flight.set_flight_details(details)
            flightdetail = f"from: {flight.origin_airport_name}, {flight.origin_airport_country_name}\n" \
                           f"to: {flight.destination_airport_name}, {flight.destination_airport_country_name}"
            if flight.altitude > 7000:
                height = "hight in the air"
            else:
                if flight.time + TWENTY_MINS_IN_SEC > flight.time_details['estimated']['arrival']:
                    height = "landing"
                else:
                    height = "take-off"
            print(f"{flightdetail}\n{height}\n_______________________________________")
            toast = Notification(
                app_id="Look out of the Window!",
                title=f"{flight.number}, {height}",
                msg=flightdetail,
                duration='long',

            )
            toast.add_actions(label="more details",
                              launch=f"https://www.flightradar24.com/{flight.id}")
            toast.show()

        except:
            print("No details available\n____________________________")


def main() -> None:
    radar = AirplanesInfrontWindow()
    radar.set_weather()
    if radar.new_flight_in_area():
        radar.print_flights()


if __name__ == '__main__':
    main()
