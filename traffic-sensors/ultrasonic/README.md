# ULTRASONIC sensor

## HC-SR04 sensor

Parameters:
* 5V DC
* 2cm-500cm
* 0.3cm resolution
* 40 kHz

pins:
* Vcc
* Trig
* Echo
* GND

## HC-SR04-RPi interface

HC-SR04 sensor runs on 5V, whereas on RPi pins can appear only 3V, therefore there is need for voltage divider

```
Vcc   o-----------------------o 5V

Trig  o-----------------------o  GPIO OUT

Echo  o---------|
               R1
                |
                o-------------o  GPIO IN
                |
               R2
                |
GND   o---------o-------------o  GND

Vgpio = Vecho (R2/(R1+R2))

```

## Princip of sensor

On trigger is sent signal of length 10
