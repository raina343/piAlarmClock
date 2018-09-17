import Adafruit_CharLCD as LCD
import Adafruit_GPIO.MCP230xx as MCP
gpio = MCP.MCP23017()
lcd = LCD.Adafruit_RGBCharLCD(0, 1, 2, 3, 4, 5,16, 2, 6, 7, 8,gpio=gpio)

