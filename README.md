# GOPRO_TIMELAPSE

## Installation

Update 
```cmd
sudo apt-get update && sudo apt-get upgrade
```

Create a virtual environment and activate it
```cmd
cd GOPRO_TIMELAPSE
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:
```cmd
pip install -r requirements.txt
```

## Connect to GoPro

1. Go to "Preferences" --> "Connections" --> "Connect Device" --> "GoPro App"
2. Tap on the "info icon"
3. Remember **Camera Name** and **Password**
4. Update wpa_supplicant.conf

```cmd
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=CH

network={
        ssid="GP26******"
        psk="*********"
}
```
Reconfigure the interface
```cmd
wpa_cli -i wlan0 reconfigure
```
You can verify whether it has successfully connected using `ifconfig wlan0`
