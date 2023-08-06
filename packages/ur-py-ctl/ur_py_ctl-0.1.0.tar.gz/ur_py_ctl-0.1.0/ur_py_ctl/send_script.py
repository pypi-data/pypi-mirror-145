import logging
import socket

import ur_py_ctl.urscript_commands as ur_cmd
from ur_py_ctl import LOG_DIR

SERVER_ADRESS = "192.168.101.102"
SERVER_PORT = 30003
UR_IP = "192.168.101.101"
UR_SERVER_PORT = 30002
# TOOL_ANGLE_AXIS = [-68.7916, -1.0706, 100, 3.1416, 0.0, 0.0]

# New tool angle
TOOL_ANGLE_AXIS = [0, 0, 0, 0, 0.0, 0.0]

# UTIL

logging.basicConfig(
    filename=LOG_DIR / "send_script.log", filemode="a", level=logging.DEBUG
)


def start_log() -> None:
    logging.debug("Start script")
    logging.debug("GLOBALS")
    logging.debug("SERVER_ADRESS: {}".format(SERVER_ADRESS))
    logging.debug("SERVER_PORT: {}".format(SERVER_PORT))
    logging.debug("UR_IP: {}".format(UR_IP))
    logging.debug("UR_SERVER_PORT: {}".format(UR_SERVER_PORT))
    logging.debug("TOOL_ANGLE_AXIS: {}".format(TOOL_ANGLE_AXIS))


def get_script() -> bytes:
    script = ""
    script += "def program():\n"
    script += ur_cmd.set_tcp(0, 0, 0, 0, 0, 0)

    script += ur_cmd.textmsg("Starting")

    for i in range(10):

        script += ur_cmd.move_to_pose(i * 0.2, 0, 500, 0, 0, 0, v=50 / 1000, r=5 / 1000)
        script += ur_cmd.textmsg(f"Sending command number: {i}")

    script += f'\tsocket_open("{SERVER_ADRESS}", {SERVER_PORT})\n'
    script += ur_cmd.textmsg("End program")
    script += '\tsocket_send_string("c")\n'
    script += "\tsocket_close()\n"
    script += "end\n"
    script += "program()\n\n\n"

    return script.encode()


def send_script() -> None:
    start_log()

    send_socket = socket.create_connection((UR_IP, UR_SERVER_PORT), timeout=2)
    send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    logging.debug("Sockets setup")

    script = get_script()
    print("Sending commands")

    # send file
    send_socket.send(script)
    logging.debug("File sent")

    # make server
    recv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to the port
    recv_socket.bind((SERVER_ADRESS, SERVER_PORT))

    # Listen for incoming connections
    recv_socket.listen(1)
    while True:
        logging.debug("Waiting for accept")
        _, client_address = recv_socket.accept()
        logging.debug(f"Recieved accept from: {client_address}")
        break

    recv_socket.close()

    send_socket.close()
    print("Program done ...")
