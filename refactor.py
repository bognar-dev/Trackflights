from winotify import Notification, audio
from FlightRadar24.api import FlightRadar24API

# flightradar setup
fr_api = FlightRadar24API()

# winotify setup
toast = Notification(app_id="Look out the window!", title="")
toast.set_audio(audio.Default, loop=False)


def set_weather():
    sunny = int(input("Please Choose your weather.\n(1) Sunny (0) Cloudy\n"))
    return bool(sunny)


def flightsinmonchengladbachsunny():
    monchengladbach = {'tl_y': 51.186454, 'tl_x': 6.363371, 'br_y': 51.102381, 'br_x': 6.578291}
    bounds_mgl = fr_api.get_bounds(monchengladbach)
    flights = fr_api.get_flights(bounds=bounds_mgl)

    return flights


def flightsinmonchengladbachCloudy():
    monchengladbach = {'tl_y': 51.186454, 'tl_x': 6.363371, 'br_y': 51.102381, 'br_x': 6.578291}
    bounds_mgl = fr_api.get_bounds(monchengladbach)
    flights = fr_api.get_flights(bounds=bounds_mgl)
    for flight in flights:
        if flight.altitude >= 7000:
            flights.remove(flight)

    return flights


def new_flight_in_area():
    len(flights) > len(flights_old)
    #TODO: Make function


def print_flights(flights, flights_old):
    TWENTY_MINS_IN_SEC = 1200
    newest_flight = flights[-1];
    # TODO: Make console output correct
    if new_flight_in_area():
        print("New flight")
        details = fr_api.get_flight_details(flight_id=newest_flight.id)
        try:
            newest_flight.set_flight_details(details)
            flightdetail = f"from: {newest_flight.origin_airport_name}, {newest_flight.origin_airport_country_name}\n" \
                           f"to: {newest_flight.destination_airport_name}, {newest_flight.destination_airport_country_name}"
            if newest_flight.altitude <= 6000:
                if newest_flight.time + TWENTY_MINS_IN_SEC > newest_flight.time_details['estimated']['arrival']:
                    height = "landing"
                else:
                    height = "take-off"
            else:
                height = "high in the air"
            print(f"{flightdetail}\n{height}\n_______________________________________")
            toast = Notification(
                app_id="Look out of the Window!",
                title=f"{newest_flight.number}, {height}",
                msg=flightdetail,
                duration='long',

            )
            toast.add_actions(label="more details",
                              launch=f"https://www.flightradar24.com/{newest_flight.id}")
            toast.show()

        except:
            print("No details available\n____________________________")
        flights_old = flights

    else:
        flights_old = flights
        return flights_old

if __name__ == '__main__':
    sunny = set_weather()
    flights_old = []
    flights = []
    while True:
        while sunny:
            flights = flightsinmonchengladbachsunny()
            flights_old = print_flights(flights, flights_old)
        while not sunny:
            flights = flightsinmonchengladbachCloudy()
            flights_old = print_flights(flights, flights_old)
