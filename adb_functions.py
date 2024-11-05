import os
from adb_shell.adb_device import AdbDeviceTcp
from adb_shell.auth.sign_pythonrsa import PythonRSASigner
from adb_shell.auth.keygen import keygen


class ADBConnection:
    def __init__(self,
                 ip,
                 port=5555,
                 adbkey_path="adbkey",
                 adbkey_pub_path="adbkey.pub"):
        """
        Initialize the ADB connection to an Android device.

        :param ip: The IP address of the Android device.
        :param port: The port for ADB connection (default is 5555).
        :param adbkey_path: Path to the private key for ADB authentication.
        :param adbkey_pub_path: Path to the public key for ADB authentication.
        """
        self.ip = ip
        self.port = port
        self.device = None
        self.signer = self._load_or_generate_signer(
            adbkey_path, adbkey_pub_path)

    def _load_or_generate_signer(self, adbkey_path, adbkey_pub_path):
        """Load or generate RSA keys using adb_shell.auth.keygen."""
        print(os.path.exists(adbkey_path))
        if (os.path.exists(adbkey_path) is False or
                os.path.exists(adbkey_pub_path) is False):
            print("generating keys...")
            keygen(adbkey_path)  # Generates both private and public keys

        with open(adbkey_path, 'rb') as f:
            private_key = f.read()
        with open(adbkey_pub_path, 'rb') as f:
            public_key = f.read()

        return PythonRSASigner(public_key.decode(), private_key.decode())

    def connect(self):
        """Connect to the Android device over ADB."""
        self.device = AdbDeviceTcp(self.ip, self.port)
        connected = self.device.connect(
            rsa_keys=[self.signer], auth_timeout_s=0.1)
        if connected:
            print(f"Connected to {self.ip}:{self.port}")
        else:
            print(f"Failed to connect to {self.ip}:{self.port}")
        return connected

    def disconnect(self):
        """Disconnect from the Android device."""
        if self.device:
            self.device.close()
            print("Disconnected from device.")
            self.device = None

    def run_shell_command(self, command):
        """
        Run a shell command on the Android device.

        :param command: The shell command to run.
        :return: The output of the command.
        """
        if not self.device:
            raise ConnectionError(
                "Device not connected. Please connect first.")

        output = self.device.shell(command)
        return output

    def send_click(self, click_data):

        if len(click_data) == 2:
            self.device.shell(f'input tap {click_data[0]} {click_data[1]}')
            return
        elif len(click_data) == 3:
            x1, y1, duration = click_data
            x2 = x1
            y2 = y1
        elif len(click_data) == 5:
            x1, y1, x2, y2, duration = click_data

        self.device.shell("input swipe {x1} {y1} {x1} {y1} {duration}")


def get_device():
    TEST_PORT = 5571  # MAIN ACCT PORT
    # TEST_PORT = 5586 # FL PORT
    adb_connection = ADBConnection(ip="192.168.0.198", port=TEST_PORT)
    # Connect to the device
    if adb_connection.connect():
        device = adb_connection.device

        return device

    return None


device = get_device()
