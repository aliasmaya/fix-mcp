from datetime import datetime
from typing import Dict

class FIXMessage:
    def __init__(self, seq_num: int, sender: str, target: str, msg_type: str):
        self.fields = {}
        self.begin_string = "FIX.4.2"
        self.msg_type = msg_type
        self.sender_comp_id = sender
        self.target_comp_id = target
        self.msg_seq_num = seq_num
        self.sending_time = datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f")[:-3]

    def set_field(self, tag: int, value: str):
        self.fields[tag] = value

    def to_string(self) -> str:
        self.fields[8] = self.begin_string  # BeginString
        self.fields[35] = self.msg_type    # MsgType
        self.fields[49] = self.sender_comp_id  # SenderCompID
        self.fields[56] = self.target_comp_id  # TargetCompID
        self.fields[34] = str(self.msg_seq_num)  # MsgSeqNum
        self.fields[52] = self.sending_time  # SendingTime

        message = []
        for tag in sorted(self.fields.keys()):
            message.append(f"{tag}={self.fields[tag]}")
        
        result = "\001".join(message)
        checksum = sum(ord(c) for c in result) % 256
        result += f"\00110={checksum:03d}\001"
        return result
    
    def parse_message(self, message: str) -> Dict[int, str]:
        """Parse a FIX message into a dictionary of tag-value pairs."""
        fields = {}
        for field in message.split("\001"):
            if "=" in field:
                tag, value = field.split("=", 1)
                fields[int(tag)] = value
        return fields