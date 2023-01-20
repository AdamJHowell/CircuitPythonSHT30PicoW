# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time

import adafruit_sht31d
import board
import busio

"""
pip install adafruit-circuitpython-sht31d
"""

sht_temp = [21.12, 21.12, 21.12]
sht_humidity = [21.12, 21.12, 21.12]


def add_value( input_list, value ):
  """
  This will copy element 1 to position 2,
  move element 0 to position 1,
  and add the value to element 0
  :param input_list: the list to add a value to
  :param value: the value to add
  """
  if len( input_list ) == 3:
    input_list[2] = input_list[1]
    input_list[1] = input_list[0]
    input_list[0] = value
  else:
    print( f"Input list is not the expected size: {input_list}" )


def average_list( input_list ):
  """
  This will calculate the average of all numbers in a List
  :param input_list: the List to average
  :return: the average of all values in the List
  """
  return sum( input_list ) / len( input_list )


def c_to_f( value ):
  return value * 1.8 + 32


def poll_sensors():
  add_value( sht_temp, sht30_sensor.temperature )
  add_value( sht_humidity, sht30_sensor.relative_humidity )


def infinite_loop():
  loop_count = 0
  sensor_interval = 15
  last_sensor_poll = 0
  heater_interval = 20
  last_heater_run = 0
  poll_sensors()
  poll_sensors()
  while True:
    if (time.time() - last_sensor_poll) > sensor_interval:
      loop_count += 1
      poll_sensors()
      print()
      print( f"SHT30 temperature: {average_list( sht_temp ):.2f} C, {c_to_f( average_list( sht_temp ) ):.2f} F" )
      print( f"SHT30 humidity: {average_list( sht_humidity ):.1f} %" )
      print( f"Loop count: {loop_count}" )
      last_sensor_poll = time.time()
    if (time.time() - last_heater_run) > heater_interval:
      sht30_sensor.heater = True
      print( f"Sensor Heater status = {sht30_sensor.heater}" )
      time.sleep( 1 )
      sht30_sensor.heater = False
      print( f"Sensor Heater status = {sht30_sensor.heater}" )
      last_heater_run = time.time()


if __name__ == "__main__":
  i2c = busio.I2C( board.GP5, board.GP4 )
  sht30_sensor = adafruit_sht31d.SHT31D( i2c )
  infinite_loop()
