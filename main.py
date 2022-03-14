# flightradar setup
import tkinter

from FlightRadar24.api import FlightRadar24API

fr_api = FlightRadar24API()

# winotify setup
from winotify import Notification, audio

toast = Notification(app_id="Look out the window!", title="")
toast.set_audio(audio.Reminder, loop=False)

#tkinter setup
from tkinter import *
from tkinter import messagebox
win = Tk()
win.title('Flights')
win.geometry("200x200")
win.resizable(0,0)
def setsunny():
    sunny = True
    messagebox.showinfo("Changed weather condition", "You set the weather to sunny")
    return sunny
def setcloudy():
    sunny = False
    messagebox.showinfo("Changed westher condition", "You set the weather to cloudy")
    return sunny
buttonSunny = tkinter.Button(win, text='Sunny', command = setsunny,width= 10)
buttonCloudy = tkinter.Button(win, text='Cloudy', command= setcloudy,width= 10)

def flightsinmonchengladbachSunny():
    monchengladbach = {'tl_y': 51.186454, 'tl_x': 6.363371, 'br_y': 51.102381, 'br_x': 6.578291}
    bounds_mgl = fr_api.get_bounds(monchengladbach)
    flights = fr_api.get_flights(bounds=bounds_mgl)

    return flights
def flightsinmonchengladbachCloudy():
    monchengladbach = {'tl_y': 51.186454, 'tl_x': 6.363371, 'br_y': 51.102381, 'br_x': 6.578291}
    bounds_mgl = fr_api.get_bounds(monchengladbach)
    flights = fr_api.get_flights(bounds=bounds_mgl)

    return flights


def checkflights(flights, flights_old):
    if len(flights) != len(flights_old):
        print("New flight")
        for flight in flights:
            details = fr_api.get_flight_details(flight_id=flight.id)
            try:
                flight.set_flight_details(details)
                flightdetail = f"from: {flight.origin_airport_name}, {flight.origin_airport_country_name}\n " \
                               f" to: {flight.destination_airport_name}, {flight.destination_airport_country_name}"
                print(flightdetail)
                toast = Notification(
                    app_id="Look out of the Window!",
                    title=flight.number,
                    msg=flightdetail,
                    duration='short',
                    icon=r"C:\Users\nikla\Documents\Studium\Niki\GDI\flights\airplane.ico"

                )
                toast.add_actions(label="more details",
                                  launch=f"https://www.flightradar24.com/{flight.id}")
                toast.show()

            except:
                print("No details available")
        flights_old = flights
    else:
        flights_old = flights
    return flights, flights_old


if __name__ == '__main__':
    flights_old = []
    flights = []
    sunny = True
    buttonSunny.pack()
    buttonCloudy.pack()
    win.mainloop()
    while True:
        while sunny:
            flights = flightsinmonchengladbachSunny()
            flights, flights_old = checkflights(flights, flights_old)
        while not sunny:
            print("not sunny")
            flights = flightsinmonchengladbachCloudy()
            flights, flights_old = checkflights(flights, flights_old)
