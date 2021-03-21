#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dynamixel_sdk
import alphabeta
import sys

# Control table address
ADDR_PRO_TORQUE_ENABLE      = 64
ADDR_PRO_GOAL_POSITION      = 116
ADDR_PRO_PRESENT_POSITION   = 132

# Protocol version
PROTOCOL_VERSION            = 2.0

# Default setting
BAUDRATE                    = 57600

TORQUE_ENABLE               = 1
TORQUE_DISABLE              = 0

DXL_MINIMUM_POSITION_VALUE  = 10
DXL_MAXIMUM_POSITION_VALUE  = 4000
DXL_MOVING_STATUS_THRESHOLD = 0

ID_AZ                       = 1
ID_EL                       = 2

SYNC_MOVE                   = False

def degrees_to_count(deg):
    return int((float(deg) / 0.0879) + 2048.0)

device_name = input('Enter device name (COM1, /dev/ttyUSB0, ...): ')

port_handler = dynamixel_sdk.PortHandler(device_name)
packet_handler = dynamixel_sdk.PacketHandler(PROTOCOL_VERSION)

print('Connecting to %s ...' % device_name, end='')
if port_handler.openPort():
    print(' done.')
else:
    print(' connection failed.')
    sys.exit(-1)

port_handler.setBaudRate(BAUDRATE)

def handle_result(dxl_comm_result, dxl_error):
    if dxl_comm_result != dynamixel_sdk.COMM_SUCCESS:
        print('%s' % packet_handler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print('%s' % packet_handler.getRxPacketError(dxl_error))

def go_motor(id, deg):

    count = degrees_to_count(deg)
    
    dxl_comm_result, dxl_error = packet_handler.write4ByteTxRx(
        port_handler, id, ADDR_PRO_GOAL_POSITION, degrees_to_count(deg))
    handle_result(dxl_comm_result, dxl_error)

    while SYNC_MOVE:
        pos, dxl_comm_result, dxl_error = packet_handler.read4ByteTxRx(
            port_handler, id, ADDR_PRO_PRESENT_POSITION)
        handle_result(dxl_comm_result, dxl_error)
        if pos == count:
            return

def go(az_el):
    print('Moving ...', end='')
    go_motor(ID_AZ, az_el[0])
    go_motor(ID_EL, az_el[1])
    print(' done.')

for id in [ID_AZ, ID_EL]:
    dxl_comm_result, dxl_error = packet_handler.write1ByteTxRx(
        port_handler, id, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)
    handle_result(dxl_comm_result, dxl_error)

while True:

    alpha_str = input('Enter goal alpha (degrees): ')
    beta_str = input('Enter goal beta (degrees): ')
    alpha_beta = [float(alpha_str), float(beta_str)]
    az_el = alphabeta.alpha_beta_to_az_el(alpha_beta)
    print('[alpha, beta] = %s --> [az, el] = %s' % (alpha_beta, az_el))
    go(az_el)
