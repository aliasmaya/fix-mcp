import socket
import select
import time
import logging
from typing import Optional, Dict
from fixTypes import FIXMessage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FIXClient:
    def __init__(self, host: str, port: int, sender: str, target: str, heartbt_int: int = 30):
        self.host = host
        self.port = port
        self.heartbt_int = heartbt_int
        self.socket: Optional[socket.socket] = None
        self.is_connected = False
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 5
        self.reconnect_delay = 5
        self.msg_seq_num = 1
        self.sender_comp_id = sender
        self.target_comp_id = target
        self.last_order_id = None  # To track the last order for matching Execution Report

    def connect(self) -> bool:
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(10)
            self.socket.connect((self.host, self.port))
            self.is_connected = True
            self.reconnect_attempts = 0
            logger.info(f"Connected to {self.host}:{self.port}")
            return True
        except Exception as e:
            self.is_connected = False
            self.reconnect_attempts += 1
            logger.error(f"Connection failed: {e}. Attempt {self.reconnect_attempts}")
            if self.reconnect_attempts < self.max_reconnect_attempts:
                time.sleep(self.reconnect_delay)
                return self.connect()
            return False

    def disconnect(self):
        if self.socket:
            self.socket.close()
        self.is_connected = False
        logger.info("Disconnected from server")

    def send_fix_message(self, msg_type: str, fields: Dict[int, str] = None) -> str:
        if not self.is_connected:
            if not self.connect():
                logger.info("Connection failed")
                return None

        msg = self._build_fix_message(msg_type, fields)
        try:
            self.socket.send(msg.encode())
            logger.info(f"Sent FIX message: {msg}")
            self.msg_seq_num += 1

            if msg_type == "D":  # New Order Single
                self.last_order_id = fields.get(11, f"ORDER{self.msg_seq_num}")  # ClOrdID
                return self.wait_for_execution_report(self.last_order_id)

            return "Message sent successfully"
        except Exception as e:
            logger.error(f"Error sending FIX message: {e}")
            self.is_connected = False
            return None

    def _build_fix_message(self, msg_type: str, fields: Dict[int, str] = None) -> str:
        fix_msg = FIXMessage(self.msg_seq_num, self.sender_comp_id, self.target_comp_id, msg_type)
        if fields:
            for tag, value in fields.items():
                fix_msg.set_field(tag, value)
        return fix_msg.to_string()

    def receive_fix_message(self) -> Optional[str]:
        if not self.is_connected:
            if not self.connect():
                return None

        try:
            ready = select.select([self.socket], [], [], 10)  # Increased timeout for waiting
            if ready[0]:
                data = self.socket.recv(4096).decode()
                logger.info(f"Received FIX message: {data}")
                return data
            return None
        except Exception as e:
            logger.error(f"Error receiving FIX message: {e}")
            self.is_connected = False
            return None

    def wait_for_execution_report(self, order_id: str, timeout: int = 30) -> str:
        """Wait for an Execution Report (MsgType 8) for the given order ID."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            message = self.receive_fix_message()
            if message:
                fields = FIXMessage(0, "", "", "").parse_message(message)
                if fields.get(35) == "8":  # Execution Report
                    if fields.get(37) == order_id or fields.get(11) == order_id:  # OrderID or ClOrdID
                        exec_type = fields.get(150, "0")  # ExecType
                        exec_status = fields.get(39, "0")  # OrdStatus
                        return self.parse_execution_result(exec_type, exec_status, fields)
            time.sleep(0.1)  # Small delay to prevent tight looping
        return "Timeout waiting for Execution Report"

    def parse_execution_result(self, exec_type: str, exec_status: str, fields: Dict) -> str:
        """Parse the Execution Report to determine success."""
        status_map = {
            "0": "New", "1": "Partial Fill", "2": "Fill", "4": "Canceled", "8": "Rejected"
        }
        result = f"Execution Report: Type={exec_type}, Status={status_map.get(exec_status, 'Unknown')}"
        if exec_status in ["2", "1"]:  # Fill or Partial Fill
            result += f", Filled Qty={fields.get(32, '0')}, Avg Price={fields.get(44, '0')}"
            return "Order executed successfully" + result
        elif exec_status == "8":
            return "Order rejected: " + result
        else:
            return "Order status: " + result
        
    def send_logout(self) -> str:
        """Send a FIX Logout message."""
        fields = {58: "User requested logout"}  # Text (optional)
        return self.send_fix_message("5", fields)

    def send_test_request(self, test_req_id: str) -> str:
        """Send a FIX Test Request message to check connectivity."""
        fields = {112: test_req_id}  # TestReqID
        return self.send_fix_message("1", fields)

    def send_resend_request(self, begin_seq_no: int, end_seq_no: int) -> str:
        """Send a FIX Resend Request to request message retransmission."""
        fields = {7: str(begin_seq_no), 16: str(end_seq_no)}  # BeginSeqNo, EndSeqNo
        return self.send_fix_message("2", fields)

    def send_session_reject(self, ref_seq_no: int, reject_reason: int) -> str:
        """Send a FIX Session Level Reject for invalid messages."""
        fields = {45: str(ref_seq_no), 373: str(reject_reason)}  # RefSeqNum, SessionRejectReason
        return self.send_fix_message("3", fields)

    def send_sequence_reset(self, new_seq_no: int, gap_fill_flag: bool = False) -> str:
        """Send a FIX Sequence Reset (Gap Fill) to reset sequence numbers."""
        fields = {36: str(new_seq_no)}  # NewSeqNo
        if gap_fill_flag:
            fields[123] = "Y"  # GapFillFlag
        return self.send_fix_message("4", fields)
