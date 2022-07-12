"""Pin definitions for the siemens_iot2050."""

from adafruit_blinka.microcontroller.am65xx import pin

# Digital Pins
D0 = pin.D0
D1 = pin.D1
D2 = pin.D2
D3 = pin.D3
D4 = pin.D4
D5 = pin.D5
D6 = pin.D6
D7 = pin.D7
D8 = pin.D8
D9 = pin.D9
D10 = pin.D10
D11 = pin.D11
D12 = pin.D12
D13 = pin.D13
D14 = pin.D14
D15 = pin.D15
D16 = pin.D16
D17 = pin.D17
D18 = pin.D18
D19 = pin.D19

# Analog Pins
A0 = pin.A0
A1 = pin.A1
A2 = pin.A2
A3 = pin.A3
A4 = pin.A4
A5 = pin.A5

# pin list seems not complete ?
# Output Pins are the same as Arduino Uno, two SCL and SDA Pins available and Overall 31 + 1 Pins !

# I2C allocation
SCL = pin.I2C_SCL
SDA = pin.I2C_SDA

# SPI allocation
SCLK= pin.SPIO_SCLK
MOSI = pin.SPIO_MOSI
MISO = pin.SPIO_MISO

# UART allocation
UART_TX = pin.UART0_TXD
UART_RX = pin.UART0_RXD

# PWM allocation
PWM_4 = pin.PWM_4
PWM_5 = pin.PWM_5
PWM_6 = pin.PWM_6
PWM_7 = pin.PWM_7
PWM_8 = pin.PWM_8
PWM_9 = pin.PWM_9
