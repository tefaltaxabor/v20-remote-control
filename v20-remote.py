from pymodbus.client import ModbusTcpClient

import time

client = ModbusTcpClient( 

    host = "192.168.1.202", #static IP

    port = 502,  # Default Modbus TCP port        

)



def read_register(register,SCALING_FACTOR):



    """Reads a specific Modbus register.(FC3 - Read Holding Registers)"""

    

    response = client.read_holding_registers(register - 40001,count=1, slave=1)



    if response.isError():



        print(f"Error reading register {register}")



        return None



    else:

        #8 byte  

        value = response.registers[0] / SCALING_FACTOR  # Apply scaling



        print(f"Register {register} value: {value} Hz")



        return value

def write_single_register(register, value):



    """Writes a single register using Modbus Function Code 6 (FC6)."""

    

    module_adress = register - 40001

    response = client.write_register(module_adress, value, slave=1)



    if response.isError():



        print(f"Error writing to register {register}")



    else:



        print(f"Successfully wrote {value} to register {register}")





def go_forward():

    print("Introdce desire speed (0-100)%:")

    speed_per = int(input())

    value = int(speed_per * 16384 / 100)

    write_single_register(40101,value)

    time.sleep(1)  # Wait for the command to take effect

    write_single_register(40100, 1279)  # Start command

    print (f"Moving forward at {speed_per}% speed.")



def stop():

    write_single_register(40100, 1278)  # Stop command

    print("Stopping the motor.")

def direction():

    direction = input("Enter direction (1 for clockwise, 0 for anticlockwise): ")

    if direction in ['1', '0']:

        write_single_register(40005, int(direction))

        print(f"Changed direction to {'forward' if direction == '1' else 'reverse'}")

        write_single_register(40006, 1)  # Start command

    else:

        print("Invalid direction! Please enter 1 or 0.")





def main():

    if not client.connect():



        print("Unable to connect to the Modbus server")



        return

    write_single_register(40100, 1278) #establish connection

    print("Connection established. You can now read and write registers.")

    try:

        while True:

            print("1. Start")

            print("2. Direction")

            print("3. Stop")

            print("4. Exit")

            choice = input("Enter your choice (1-4): ")

            if choice == '1':

                go_forward()

            elif choice == '2':

                direction()

            elif choice == '3': 

                stop()

            elif choice == '4':

                print("Exiting the program.")

                stop()

                break

            else:

                print("Invalid choice. Please enter 1, 2, 3 or 4.")    

    except Exception as e:

        print(f"An error occurred: {e}")

    finally:

        client.close()

        print("Connection closed.")



if __name__ == "__main__":



    main()