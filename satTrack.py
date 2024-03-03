import tkinter as tk
from skyfield.api import load, Topos
import geocoder


# Function to get user's location and update satellite position
def update_satellite_position():
    # Get user's location using IP address
    user_location = geocoder.ip("me")

    # Set latitude and longitude from user's location
    observer = Topos(
        latitude_degrees=user_location.latlng[0],
        longitude_degrees=user_location.latlng[1],
    )

    ts = load.timescale()
    t = ts.now()

    # Load TLE data for selected satellite
    selected_satellite_name = selected_satellite.get()
    satellites = load.tle_file("stations.txt")
    by_name = {sat.name: sat for sat in satellites}

    try:
        satellite = by_name[selected_satellite_name]

        # Get the position of the selected satellite
        difference = satellite - observer
        topocentric = difference.at(t)
        alt, az, d = topocentric.altaz()

        # Update GUI with the satellite position
        output_label.config(
            text=f"{selected_satellite_name} Position\nAltitude: {alt.degrees:.2f}°\nAzimuth: {az.degrees:.2f}°"
        )
    except KeyError:
        output_label.config(
            text=f"Invalid satellite selection: {selected_satellite_name} not found in TLE data"
        )

    # Schedule the function to run again after a delay (in milliseconds)
    root.after(1000, update_satellite_position)


# Function to handle satellite selection
def on_satellite_selected(*args):
    update_satellite_position()


# Create the GUI window
root = tk.Tk()
root.title("Satellite Tracker")

# Set the initial size of the GUI window (width x height)
root.geometry("400x250")

# Label to display the satellite position
output_label = tk.Label(root, text="")
output_label.pack()

# Dropdown menu for satellite selection
satellites = ["ISS (ZARYA)", "NOAA 20", "GOES 16"]  # Add more satellites as needed
selected_satellite = tk.StringVar(root)
selected_satellite.set(satellites[0])  # Set the default satellite
satellite_dropdown = tk.OptionMenu(
    root, selected_satellite, *satellites, command=on_satellite_selected
)
satellite_dropdown.pack(pady=10)

# Button to close the app
exit_button = tk.Button(root, text="Exit", command=root.destroy)
exit_button.pack()

# Start updating the satellite position
update_satellite_position()

# Run the GUI event loop
root.mainloop()
