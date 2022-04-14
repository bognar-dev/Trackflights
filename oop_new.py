from winotify import Notification
from FlightRadar24.api import FlightRadar24API

# flightradar setup
fr_api = FlightRadar24API()


class Radar:

    def __init__(self):
        self.area = {}
        self.sunny = False
        self.flights = {}

    def get_flights(self):
        self.flights = fr_api.get_flights(bounds=self.area)

    def set_area(self):
        self.sunny = bool(input("Please Choose your weather.\n======================\n(1) Sunny (0) Cloudy"
                       "\n======================\n"))
        print("======================")
        if self.sunny is True:
            self.area = fr_api.get_bounds({'tl_y': 52.186454, 'tl_x': 6.363371, 'br_y': 51.102381, 'br_x': 6.578291})
        if self.sunny is False:
            self.area = fr_api.get_bounds({'tl_y': 51.186454, 'tl_x': 6.363371, 'br_y': 51.102381, 'br_x': 6.578291})


class Flight:
    def __init__(self, r, counter):
        self.details = ""
        self.counter = counter
        self.flight = r.flights[self.counter]
        self.flightdetail = ""
        self.height = ""

    def set_details(self):
        TWENTY_MINS_IN_SEC = 1200
        self.details = fr_api.get_flight_details(flight_id=self.flight.id)
        try:
            self.details = self.flight.set_flight_details(self.details)
            self.flightdetail = f"from: {self.flight.origin_airport_name}, {self.flight.origin_airport_country_name}\n"\
                        f"to: {self.flight.destination_airport_name}, {self.flight.destination_airport_country_name} "
            if self.flight.altitude > 7000:
                self.height = "hight in the air"
            else:
                if self.flight.time + TWENTY_MINS_IN_SEC > self.flight.time_details['estimated']['arrival']:
                    self.height = "landing"
                else:
                    self.height = "take-off"
        except:
            print("No details available")

    def flight_notification(self):
        print(f"{self.flightdetail}\n{self.height}\n_________________________________")
        toast = Notification(
            app_id="Look out of the Window!",
            title=f"{self.flight.number}, {self.height}",
            msg=self.flightdetail,
            duration='long',

        )
        toast.add_actions(label="more details",
                          launch=f"https://www.flightradar24.com/{self.flight.id}")
        toast.show()


def main() -> None:
    radar = Radar()
    radar.set_area()
    counter = 0
    while True:
        radar.get_flights()
        while counter < len(radar.flights):
            flight = Flight(r=radar, counter=counter)
            flight.set_details()
            flight.flight_notification()
            counter += 1
        if len(radar.flights) != len(radar.get_flights()):
            counter = 0


if __name__ == '__main__':
    main()
