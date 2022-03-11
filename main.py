from FlightRadar24.api import FlightRadar24API
#from win10toast_click import ToastNotifier
import webbrowser
from winotify import Notification, audio

fr_api = FlightRadar24API()
#toast = ToastNotifier()
toast = Notification(app_id="Look out the window!",title="")
toast.set_audio(audio.Reminder, loop=False)


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


def checkflights(flights, flights_old):
    print(len(flights))
    if len(flights) != len(flights_old):
        print("New flight")
        for flight in flights:
            details = fr_api.get_flight_details(flight_id=flight.id)
            try:
                flight.set_flight_details(details)
                flightdetail = f"from: {flight.origin_airport_name},{flight.origin_airport_country_name}, to: {flight.destination_airport_name},{flight.destination_airport_country_name}, number : {flight.number} "
                print(flightdetail)
                toast = Notification(
                    app_id="Look out the Window!",
                    title=flight.number,
                    msg=flightdetail,
                    icon=r"C:\Users\nikla\Documents\Studium\Niki\GDI\flights\airplane.ico"
                )
                toast.add_actions(label="Button text",
                                  launch=f"https://www.flightradar24.com/{flight.id}")
                '''toast.show_toast(
                    title="Look out of the window",
                    msg=flightdetail,
                    duration=5,
                    icon_path="airplane.ico",
                    threaded=True,
                    callback_on_click=webbrowser.open_new_tab(f"https://www.flightradar24.com/{flight.id}")
                )'''
            except:
                print("No details available")
        flights_old = flights
    else:
        flights_old = flights
    return flights, flights_old


if __name__ == '__main__':
    flights_old = []
    flights = []
    while True:
        flights = flightsinmonchengladbach()
        flights, flights_old = checkflights(flights, flights_old)
