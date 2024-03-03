from skyfield.api import load, Topos


def generate_stations_file():
    # Load the TLE data for the ISS from Celestrak
    satellites_url = "https://www.celestrak.com/NORAD/elements/stations.txt"
    satellites = load.tle_file(satellites_url)

    # Get the latest TLE data for the ISS
    tle_lines = satellites["ISS (ZARYA)"].text()

    # Save the TLE data to stations.txt
    with open("stations.txt", "w") as file:
        file.write(tle_lines)

    print("stations.txt has been generated successfully.")


if __name__ == "__main__":
    generate_stations_file()
