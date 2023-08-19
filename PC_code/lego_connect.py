# SKELETON AND BASIC FUNCTIONS FROM PYBRICKS TUTORIAL https://pybricks.com/projects/tutorials/wireless/hub-to-device/pc-communication/
# SPDX-License-Identifier: MIT
# Copyright (c) 2020 Henrik Blidh
# Copyright (c) 2022 The Pybricks Authors

import asyncio
from bleak import BleakScanner, BleakClient

from kociemba import run_kociemba
from pglass_algo import run_pglass_algo
import gym

UART_SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
UART_RX_CHAR_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
UART_TX_CHAR_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

# Replace this with the name of your hub if you changed
# it when installing the Pybricks firmware.
HUB_NAME = "Pybricks Hub"

#allows to wait for robot to be finished with a move to send new one
robot_done_event = asyncio.Event()
robot_setup_event = asyncio.Event()
robot_finished_event = asyncio.Event()
def hub_filter(device, ad):
    return device.name and device.name.lower() == HUB_NAME.lower()


def handle_disconnect(_):
    print("Hub was disconnected.")


async def robot_waiter(): #as from asyncio documentation
    await robot_done_event.wait()
async def robot_waiter_setup():
    await robot_setup_event.wait()
async def robot_waiter_finished():
    await robot_finished_event.wait()


def handle_rx(_, data: bytearray):
    decoded = data.decode()
    
    if(decoded == "oki"):
        print("done, moving on")
        robot_done_event.set()
    elif(decoded == "pos"):
        print("Robot setup complete.")
        robot_setup_event.set()
    elif(decoded == "DON"):
        print("done msg from robot received")
        robot_finished_event.set()


async def initialise_gym():
    env = gym.make("RubiksCube-v0")
    obs = env.reset()
    moves = env.scramble_moves
    return obs, moves


async def main():
    # Find the device and initialize client.
    device = await BleakScanner.find_device_by_filter(hub_filter)
    client = BleakClient(device, disconnected_callback=handle_disconnect)

    # Shorthand for sending some data to the hub.
    async def send(client, data):
        robot_done_event.clear()
        await client.write_gatt_char(rx_char, data)
    
   #translate list from gym to the format taken by the robot (see explanation at send_moves_robot)
    def translate_gym_to_robot(list_of_moves):
        nr_moves = len(list_of_moves)
        translated  = []
        nr_of_times = 1
        i = 0
        while i < nr_moves:
            curr = list_of_moves[i]
            if (i+1) < nr_moves and curr == list_of_moves[i+1]: #second in a row
                if (i+2) < nr_moves and curr == list_of_moves[i+2]: #third in a row
                    nr_of_times = 3
                else: nr_of_times = 2
            else: nr_of_times = 1
            res = f"{nr_of_times}" + f"{curr:02d}"
            translated.append(res)
            i += nr_of_times
        return translated
    
    
    
    def pick_unscrambling_method():
            pick = input("Please decide which unscrambling algorithm to use. Type A for pglass' beginner solver algorithm (avg. 250 moves), type B for kociemba's two-phase algorithm.\n")
            global nr_moves, solution, translated
            if pick == "A" or pick == "a":
                cube, solver, optimised, translated = run_pglass_algo(obs)
                nr_moves = len()
            elif pick =="B" or pick == "b": 
                nr_moves, solution, translated = run_kociemba(obs)
            else:
                print("Input does not match any algorithm.")
                pick_unscrambling_method()


    async def send_moves_robot(moves):
        print("moves:")
        print(moves)
        for move in moves:
            print(f"sent move {move}")
            await send(client, move.encode())
            waiter_task = asyncio.create_task(robot_waiter())
            await waiter_task


    try:
        # Connect and get services.
        await client.connect()
        await client.start_notify(UART_TX_CHAR_UUID, handle_rx)
        nus = client.services.get_service(UART_SERVICE_UUID)
        rx_char = nus.get_characteristic(UART_RX_CHAR_UUID)

        # Tell user to start program on the hub.
        print("Start the program on the hub by pressing the button.")
        setup_waiter_task = asyncio.create_task(robot_waiter_setup())
        await setup_waiter_task
        try:
            input("Place the cube in the platform. Press enter to proceed.")
        except SyntaxError:
            pass
        
        finished_waiter_task = asyncio.create_task(robot_waiter_finished())
        

        obs, scramble_moves = await initialise_gym()


        scramble_moves_translated = translate_gym_to_robot(scramble_moves)
        await send_moves_robot(scramble_moves_translated)
        await send(client, "0w8".encode()) #wait until ready to unscramble
        
        #decide on unscrambling method
        pick_unscrambling_method()
            
        print(f"found a solution in {nr_moves} moves!")


        await send_moves_robot(translated)
        await send(client, "don".encode()) #done with unscrambling
        print("done! your cube is solved")

    except Exception as e:
        # Handle exceptions.
        print(e)

    finally:
        # Disconnect when we are done.
        print("waiting on robot......")
    
        await finished_waiter_task
        print("disconnect from the hub")
        
        await client.disconnect()
        pass


# Run the main async program.
asyncio.run(main())

