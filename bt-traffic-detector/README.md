# BLUETOOTH TRAFFIC DETECTOR

This is documentation for install and using **bluetooth traffic detector** based on **Ubertooth One**

[Ubertooth GitHub](https://github.com/greatscottgadgets/ubertooth)

---
## content

* [Installation of libraries for Ubertooth](https://github.com/MojaCZ/bt-traffic-detector#installation-of-libraries-for-ubertooth)
* [Installation of BTD program](https://github.com/MojaCZ/bt-traffic-detector#installation-of-btd-program)
* [Configuration of BTD.conf file](https://github.com/MojaCZ/bt-traffic-detector#configuration-of-btd-conf-file)
* [Connecting Raspberry Pi GPIO interface](https://github.com/MojaCZ/bt-traffic-detector#connecting-raspberry-pi-gpio-interface)
* [Running BTD program](https://github.com/MojaCZ/bt-traffic-detector#running-btd-program)
* [Data processing](https://github.com/MojaCZ/bt-traffic-detector#data-processing)
* [Web imterface](https://github.com/MojaCZ/bt-traffic-detector#web-interface)

---

## Installation of libraries for Ubertooth

For installing and running Ubertooth libraries are needs this programs:

* **cmake**               tools designed to build, test and package software
* **libusb-1.0-0-dev**    library for programming USB applications
* **make**                building and maintaining groups of programs from source code.
* **gcc**                 GNU Compiler Collection (C, C++, Objective-C, Fortran, Ada, GO)
* **g++**                 C++ compiler
* **libbluetooth-dev**    development files for using the BlueZ Linux Bluetooth library

All can be installed in terminal by:

`sudo apt-get install cmake libusb-1.0-0-dev make gcc g++ libbluetooth-dev`

`pkg-config libpcap-dev python-numpy python-pyside python-qt4`

### libbtbb

Blueooth baseband library for Ubertooth tools to decode Bluetooth packages

```
wget https://github.com/greatscottgadgets/libbtbb/archive/2017-03-R2.tar.gz -O libbtbb-2017-03-R2.tar.gz
tar xf libbtbb-2017-03-R2.tar.gz
cd libbtbb-2017-03-R2
mkdir build
cd build
cmake ..
make
sudo make install
```

in case of error try run `sudo ldconfig`

### Ubertooth tools

packages for sniffing Bluetooth packets, configuring the Ubertooth and updating firmware

```
wget https://github.com/greatscottgadgets/ubertooth/releases/download/2017-03-R2/ubertooth-2017-03-R2.tar.xz -O ubertooth-2017-03-R2.tar.xz
tar xf ubertooth-2017-03-R2.tar.xz
cd ubertooth-2017-03-R2/host
mkdir build
cd build
cmake ..
make
sudo make install
```

in case of error try run `sudo ldconfig`

### Python packages

Ubertooth libraries requires numpy

`sudo apt install python-pyp
pip install numpy`

---

### Testing

To test functionality of Ubertooth try `sudo ubertooth-rx` or `sudo ubertooth-btle -p`

For sniffing bluetooth packets run `sudo ubertooth-rx -z`, this return systemtime, channel, LAP, err, ...

---

## Installation of BTD program

To run this program, you will need to have installed python3 on your computer. Then few packages like time, RPi.GPIO... . All can be installed by following installation process:

```
sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get install python3.6
sudo apt-get install -y python3-pip
pip3 install RPi.GPIO
```

RPi.GPIO library is required only for using RPi GPIO ports for input and output

For running this program, just [Download ZIP](https://github.com/MojaCZ/bt-traffic-detector/archive/master.zip) from github and ind Linux terminal run `sudo python3 BTD.py`.

---

## Configuration of BTD conf file

For configuring measurement there is BTD.conf file.

You can set:

* **CWD** Current Working Directory where the text files with measured parameters will be saved.
* **FILE_NAME_GROUP** the first part of created file name.
* **WAIT-TIME** is interval after which device address can be stored again (preventing from writing one device 1000 times in second)
* **NEW_FILE_INTERVAL** after this interval program will be restarted and new file created
* **RPI** 1 when using Raspberry Pi GPIO, 0 when using program without RPi GPIO
* **RPI_START_MEASURE** when this GPIO pin is on, program will start measurement, when is off, program will stop measurement and wait in loop till pin is on again
* **RPI_EXIT** when this GPIO pin is off, program will exit, and RPi will shutdown
* **RPI_READY** is GPIO pin number for LED signalling if RPi was started and program is ready
* **RPI_RUN** is GPIO pin number for LED signalling if measurement is in process (is reading and saving catched bluetooth devices)
* **RPI_CATCHED** is GPIO pin number for LED. LED change state every time new address is stored

There can be few possible errors when initializing program (on start, program will read BTD.conf file). These errors appear when user pass unvalidated data like if add new variable, delete some variable, give RPi GPIO pins pin which could destroy it

Errors event are:

* can't read file
* wrong format of at least one variable
* too many variables
* some var is missing
* wrong type of variable
* checks if RPI_ ports are valid
* checks if RPI_ port isn't used by other RPI_ var

---

## Connecting Raspberry Pi GPIO interface

To connect LEDs and switches to Raspberry Pi there is GPIO interface. Pins on header are numbered from one to 26 (according to board numbering). Only pins 7, 11, 12, 13, 15, 16, 18 and 22 are available for input and output and ONLY 3V CAN APPEAR ON PINS. For power there is pin 1 (3V) and for GND pin 6. Layout of pins are displayed below:

```
___________________
   3V | 1  |  2  |
      | 3  |  4  |
      | 5  |  6  | GND
 GPIO | 7  |  8  |
      | 9  |  10 |
 GPIO | 11 |  12 | GPIO
 GPIO | 13 |  14 |
 GPIO | 15 |  16 | GPIO
      | 17 |  18 | GPIO
      | 19 |  20 |
      | 21 |  22 | GPIO
      | 23 |  24 |
      | 25 |  26 |
```

---

## Running BTD program

If you have installed Python3 on your computer in location `/usr/bin/env python3`, othervise change location on first line of BTD.py file `#!/usr/bin/env python3`

If file is not executable yet, doesn't have -x when listed with `ls -l`, change mode +x: `chmod +x dir/BTD.py`

To run program, type on Linux terminal `dir/BTD.py`

Dir stands for directory of file

---

## Data processing

### Running btdProcess.py

If you have installed Python3 on your computer in location `/usr/bin/env python3`, othervise change location on first line of BTD.py file `#!/usr/bin/env python3`

If file is not executable yet, doesn't have -x when listed with `ls -l`, change mode +x: `chmod +x dir/btdProcess.py`

To run program, type on Linux terminal `dir/btdProcess.py`

Dir stands for directory of file

### Other documentation soon available

For Data processing was created Program. Documentation will be soon available

---

## Web interface

There will be added web server for Raspberry Pi for better configuration and files management system
