# CanSat Live Telemetry System

[![CanSat CI](https://github.com/chinmaymusale123/How-to-build-a-Cansat/actions/workflows/ci.yml/badge.svg)](https://github.com/chinmaymusale123/How-to-build-a-Cansat/actions/workflows/ci.yml)
[![MicroPython](https://img.shields.io/badge/MicroPython-Raspberry%20Pi%20Pico%20W-blue)](https://micropython.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An autonomous real-time atmospheric research platform built using the **Raspberry Pi Pico W**. This CanSat collects environmental, motion, and GPS data during flight and transmits live telemetry to a wireless web dashboard while simultaneously logging mission data for post-flight analysis.

---

## Overview

The CanSat Live Telemetry System is designed for high-altitude experiments, educational rocket launches, and atmospheric research. It operates autonomously, collecting and transmitting mission-critical data including temperature, pressure, altitude, orientation, and GPS location.

The system creates its own WiFi access point and hosts a live telemetry dashboard accessible from any smartphone or computer without requiring internet access.

---

## System Architecture

```
                +--------------------+
                | Raspberry Pi Pico W|
                +---------+----------+
                          |
         +----------------+----------------+
         |                |                |
      BMP280           MPU6050            GPS
  (Temp/Pressure)   (Accel/Gyro)    (Location Data)
         |                |                |
         +----------------+----------------+
                          |
                   Data Processing
                          |
            +-------------+-------------+
            |                           |
        SD Card Logging          WiFi Telemetry
            |                           |
        CSV Data Storage         Live Web Dashboard
                                 (http://192.168.4.1)
```

---

## Technical Specifications

| Component | Specification | Description |
|---|---|---|
| **Microcontroller** | Raspberry Pi Pico W | Dual-core ARM Cortex-M0+, 2.4GHz Wi-Fi |
| **Environmental Sensor** | BMP280 | Temperature, barometric pressure, calculated altitude |
| **Motion Tracking (IMU)** | MPU6050 | 3-axis accelerometer (±2g), 3-axis gyroscope (±250°/s) |
| **GPS Receiver** | UART GPS Module (9600 baud) | Latitude, Longitude, GPS Altitude, Satellites |
| **Data Storage** | MicroSD Card (SPI interface) | Autonomous CSV logging at 1 Hz |
| **Communication** | Built-in Wi-Fi Access Point | Hotspot SSID: `CANSAT_LIVE` |
| **Telemetry Interface** | Embedded Web Dashboard | Accessible at `http://192.168.4.1` |
| **Power Supply** | 3.7V - 5V Battery | Autonomous on-board battery power |

For detailed wiring and pinout instructions, see [CONNECTIONS.md](CONNECTIONS.md).

---

## Key Features

- **Environmental Monitoring:** BMP280 sensor measuring ambient temperature, atmospheric pressure, and live altitude calculation.
- **Flight Dynamics & Motion:** MPU6050 6-axis IMU measuring linear acceleration and rotational rates.
- **Geographic Tracking:** Real-time NMEA sentence parsing for latitude, longitude, satellite count, and GPS altitude.
- **Fault-Tolerant Logging:** MicroSD storage logs telemetry to `/sd/cansat_log.csv` and safely continues execution even if the SD card is disconnected.
- **Wireless Web Dashboard:** Self-hosted HTTP server auto-refreshing telemetry every second with zero client installation needed.

---

## Project Structure

```
How-to-build-a-Cansat/
├── .github/
│   └── workflows/
│       └── ci.yml               # Automated syntax and test CI pipeline
├── 3D Structures (built using fusion 360)/
│   ├── Battery_Plate.stl        # Modular battery mounting bracket
│   ├── Bottom_Cap.stl           # CanSat base enclosure
│   ├── Electronic_Plate.stl     # Sensor & Pico mounting plate
│   ├── Main_Body_Tube.stl       # Cylindrical airframe chassis
│   ├── Nose_Cone.stl            # Aerodynamic top nose cone
│   └── Parachute_Disk.stl       # Parachute attachment plate
├── Imported libraries/          # MicroPython driver modules
│   ├── bmp280.py
│   ├── micropython_tinygpsplus.py
│   ├── RPI_PICO_W-20251209-v1.27.0.uf2
│   └── sdcard.py
├── Test files/                  # Individual sensor unit tests
│   ├── Battery_test.py
│   ├── BME280_TEST.py
│   ├── gps_test.py
│   ├── main_test.py
│   ├── MPU6050_TEST.py
│   ├── SD_CARD_TEST.py
│   └── Test_Pico_W.py
├── tests/                       # Ground tooling test suite
│   └── test_log_analyzer.py
├── tools/
│   └── log_analyzer.py          # Post-flight CSV telemetry analysis tool
├── CONNECTIONS.md               # Hardware pinout guide
├── LICENSE                      # MIT License
├── main.py                      # Primary flight software entrypoint
└── README.md
```

---

## Getting Started

### 1. Flash MicroPython
Flash the included MicroPython firmware (`Imported libraries/RPI_PICO_W-*.uf2`) onto your Raspberry Pi Pico W by holding the **BOOTSEL** button while connecting via USB.

### 2. Upload Libraries & Code
Using Thonny IDE or `mpremote`:
1. Upload all files from `Imported libraries/` to the root of the Pico.
2. Upload `main.py` to the Pico.

### 3. Power On & Connect
1. Connect the battery. The Pico will start broadcasting Wi-Fi:
   - **SSID:** `CANSAT_LIVE`
   - **Password:** `12345678`
2. Connect your phone or laptop to `CANSAT_LIVE`.
3. Open any browser and navigate to:
   ```
   http://192.168.4.1
   ```

---

## Post-Flight Data Analysis

After retrieving the CanSat from flight, insert the MicroSD card into your computer and run the built-in telemetry log analyzer:

```bash
# Run log analyzer on your flight data
python tools/log_analyzer.py cansat_log.csv
```

### Example Summary Output:

```
=======================================================
  CANSAT FLIGHT TELEMETRY REPORT: cansat_log.csv
=======================================================
Total Samples Logged:    412
Valid Telemetry Frames:  412
Corrupt / Skipped Rows:  0
Total Flight Duration:   411.0 seconds
-------------------------------------------------------
ALTITUDE & APOGEE:
  Peak Altitude (Apogee): 482.3 m
  Base Altitude:          45.1 m
  Max Height Gain:        437.2 m
-------------------------------------------------------
ENVIRONMENTAL CONDITIONS:
  Temperature:           18.4 °C to 28.6 °C (Avg: 23.2 °C)
  Pressure:              955.1 hPa to 1012.4 hPa (Avg: 988.2 hPa)
-------------------------------------------------------
DYNAMICS & GPS:
  Peak Total G-Force:    3.84 g
  GPS Fixes Achieved:    398
=======================================================
```

---

## Running Verification Tests

```bash
# Run the ground station tooling tests
python -m unittest discover -s tests -p "test_*.py" -v
```

---

## 3D Printable Structure

The `3D Structures/` folder contains ready-to-print STL files for the complete modular CanSat chassis:
- **Main Body Tube:** Cylindrical outer structure conforming to standard CanSat dimensions.
- **Nose Cone:** Aerodynamic upper section.
- **Electronic Plate:** Secure mounting for Pico W and sensors.
- **Battery Plate:** Quick-release battery bracket.
- **Parachute Disk:** Recovery harness rigging ring.

---

## Authors & Contributors

- **Neeraj Kiran Janakula**  
  Creator & Lead Developer — CanSat Live Telemetry System  
  GitHub: [@Jack26-bit](https://github.com/Jack26-bit) | [LinkedIn](https://www.linkedin.com/in/neeraj-kiran-janakula-904643384)

- **Chinmay Musale**  
  Hardware Engineer & Project Manager — CanSat Live Telemetry System  
  GitHub: [@chinmaymusale123](https://github.com/chinmaymusale123) | [LinkedIn](https://www.linkedin.com/in/chinmay-musale-97b23432a)

- **Parthiban S**  
  Backend Engineer & Ground System Engineer — CanSat Live Telemetry System  
  GitHub: [@parthi1817](https://github.com/parthi1817) | [LinkedIn](https://www.linkedin.com/in/parthiban-s-588086379/)

---

## License

This project is licensed under the [MIT License](LICENSE).
