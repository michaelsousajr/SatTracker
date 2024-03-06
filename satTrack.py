import tkinter as tk
from skyfield.api import load, Topos
import geocoder
import math
import pygame
from pygame.locals import QUIT
import os


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

        # Update 2D visualization
        update_2d_visualization(alt.degrees, az.degrees)
    except KeyError:
        output_label.config(text=f"Invalid satellite selection")

    # Schedule the function to run again after a delay (in milliseconds)
    root.after(1000, update_satellite_position)


# Function to update the 2D visualization
def update_2d_visualization(altitude, azimuth):
    screen.fill((0, 0, 0))  # Clear the screen

    # Draw Earth
    earth_image = pygame.image.load(os.path.join("assets", "earth.png"))
    earth_rect = earth_image.get_rect()
    earth_rect.center = (400, 300)
    # earth_image = pygame.transform.scale(
    #    earth_image, (int(earth_rect.width * 1.5), int(earth_rect.height * 1.5))
    # )
    screen.blit(earth_image, earth_rect)

    # Draw Satellite
    satellite_image = pygame.image.load(os.path.join("assets", "satellite.png"))
    satellite_rect = satellite_image.get_rect()
    x_satellite = 400 + int(200 * math.cos(math.radians(azimuth)))
    y_satellite = 300 + int(200 * math.sin(math.radians(azimuth)))
    satellite_rect.center = (x_satellite, y_satellite)
    screen.blit(satellite_image, satellite_rect)
    pygame.display.flip()


# Function to handle satellite selection
def on_satellite_selected(*args):
    update_satellite_position()


# Create the GUI window
root = tk.Tk()
root.title("Satellite Tracker")
# Set the initial size of the GUI window (width x height)
root.geometry("300x150")

# Label to display the satellite position
output_label = tk.Label(root, text="")
output_label.pack()

satellites = [
    "ISS (ZARYA)",
    "ISS DEB",
    "CSS (TIANHE)",
    "ISS (NUAKA)",
    "FREGAT DEB",
    "CSS (WENTIAN)",
    "CSS (MENGTIAN)",
    "CREW DRAGON 7",
    "SOYUZ-MS 24",
    "SHENZOU-17 (SZ-17)",
    "PROGRESS-MS 25",
    "BEAK",
    "CLARK SAT-1",
    "TIANZHOU-7",
    "CYGNUS NG-20",
    "PROGRESS-MS 26",
    "CREW DRAGON 8",
]

selected_satellite = tk.StringVar(root)
selected_satellite.set(satellites[0])  # Set the default satellite
satellite_dropdown = tk.OptionMenu(
    root, selected_satellite, *satellites, command=on_satellite_selected
)
satellite_dropdown.pack(pady=10)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Satellite Tracker")

# Start updating the satellite position
update_satellite_position()

# Run the combined Tkinter and Pygame event loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            quit()

    pygame.display.flip()
    pygame.time.wait(10)
    root.update()
