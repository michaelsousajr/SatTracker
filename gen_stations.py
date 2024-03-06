from skyfield.api import load, Topos


def generate_stations_file():
    # Load the TLE data for the ISS from Celestrak
    satellites_url = "https://www.celestrak.com/NORAD/elements/stations.txt"
    satellites = load.tle_file(satellites_url)

    # Get the latest TLE data for the ISS
    tle_lines = satellites = [
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
    ].text()

    # Save the TLE data to stations.txt
    with open("stations.txt", "w") as file:
        file.write(tle_lines)

    print("stations.txt has been generated successfully.")


if __name__ == "__main__":
    generate_stations_file()
