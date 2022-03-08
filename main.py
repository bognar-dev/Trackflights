from FlightRadar24.api import FlightRadar24API
from win10toast import ToastNotifier
fr_api = FlightRadar24API()
toast = ToastNotifier()


def flightsinmonchengladbach():
    monchengladbach = {'tl_y': 51.186454, 'tl_x': 6.363371, 'br_y': 51.102381, 'br_x': 6.578291}
    bounds_mgl = fr_api.get_bounds(monchengladbach)
    flights = fr_api.get_flights(bounds=bounds_mgl)

    return flights


def flightsingermany():
    germany = fr_api.get_zones()['europe']['subzones']['germany']
    bounds_germany = fr_api.get_bounds(germany)
    flights = fr_api.get_flights(bounds=bounds_germany)

    return flights


if __name__ == '__main__':
    while True:
        flights = flightsinmonchengladbach()
        print(len(flights))
        if flights:
            for flight in flights:
                details = fr_api.get_flight_details(flight_id=flight.id)
                if len(flights) == len(flights):
                    try:
                        flight.set_flight_details(details)
                        flightdetail = f"Coming from: {flight.origin_airport_name}, Flying to: {flight.destination_airport_name}, number : {flight.number}"
                        print(flightdetail)
                        toast.show_toast(
                            "Look out of the window",
                            flightdetail,
                            duration=5,
                            icon_path="airplane.jpg",
                            threaded=True,
                        )

                    except:
                        print("No details available")
            flightprev = str(flight.id)