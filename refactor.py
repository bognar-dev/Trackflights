from winotify import Notification, audio
from FlightRadar24.api import FlightRadar24API

# flightradar setup
fr_api = FlightRadar24API()

# winotify setup
toast = Notification(app_id="Look out the window!", title="")
toast.set_audio(audio.Reminder, loop=False)


def set_weather():
    sunny = bool(input("Please Choose your weather.\n======================\n(1) Sunny (0) Cloudy"
                       "\n======================\n"))
    print("======================")
    return sunny


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
        if flight.altitude > 7000:
            flights.remove(flight)

    return flights


def new_flight_in_area(flights,previous_flights) -> bool:
    # Use counter and increment or decrement the counter depending on the event
    if flights == previous_flights:
        return False
    elif flights != previous_flights:
        if len(flights) > len(previous_flights):
            return True
        if len(flights) < len(previous_flights):
            return False


def print_flights(flights, flights_old):
    TWENTY_MINUTES_IN_SEC = 1200
    # TODO: Make console output correct
    if new_flight_in_area(flights, flights_old):
        print("New flight")
        for flight in flights:
            details = fr_api.get_flight_details(flight_id=flight.id)
            try:
                flight.set_flight_details(details)
                flightdetail = f"from: {flight.origin_airport_name}, {flight.origin_airport_country_name}\n" \
                               f"to: {flight.destination_airport_name}, {flight.destination_airport_country_name}"
                if flight.altitude <= 9000:
                    if flight.time + TWENTY_MINUTES_IN_SEC > flight.time_details['scheduled']['arrival']:
                        height = "landing"
                    else:
                        height = "take-off"
                else:
                    height = "high in the air"
                print(f"{flightdetail}\n{height}\n=============================")
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
                print("No details available\n==============================")
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
            flights, flights_old = print_flights(flights, flights_old)
