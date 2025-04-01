from mcp.server.fastmcp import FastMCP
from fix.client import FIXClient

from typing import Dict, Any
from dotenv import load_dotenv
import os

load_dotenv()

host = os.getenv('SELLSIDE_HOST')
if not host:
    raise ValueError('FIX Sell Side host not available')
port_src = os.getenv('SELLSIDE_PORT')
if not port_src:
    raise ValueError('FIX Sell Side port not available')
port = int(port_src)
sender = os.getenv('SENDER_COMP_ID')
target = os.getenv('TARGET_COMP_ID')
if (not sender) or (not target):
    raise ValueError('FIX sender/target COMP ID not available')

mcp = FastMCP('fix-protocol')
fix_client = FIXClient(host, port, sender, target)

@mcp.tool()
def send_fix_logon() -> Dict[str, Any]:
    """Send a FIX Logon message to the sell-side server to logon a FIX session before any actions.

    Returns:
        A dictionary containing success result and a status message
    """
    fields = {98: "0", 108: str(fix_client.heartbt_int)}  # EncryptMethod, HeartBtInt
    success = fix_client.send_fix_message("A", fields)
    return {
        "result": "success" if success else "failed",
        "message": "Logon sent successfully" if success else "Logon failed"
    }

@mcp.tool()
def send_fix_heartbeat() -> Dict[str, Any]:
    """Send a FIX Heartbeat message.
    
    Returns:
        A dictionary containing success result and a status message
    """
    success = fix_client.send_fix_message("0")
    return {
        "result": "success" if success else "failed",
        "message": "Heartbeat sent successfully" if success else "Heartbeat failed"
    }

@mcp.tool()
def send_new_order_single(symbol: str, side: str, ord_type: str, price: float, qty: int) -> Dict[str, Any]:
    """Send a New Order Single message to the sell-side server.

    Args:
        symbol: The stock symbol code
        side: The order buy/sell side, "1" for BUY while "2" for SELL
        ord_type: The order type, possible values are "1" for Market Order, "2" for Limit Order
        price: The order price
        qty: The order quantity

    Returns:
        A dictionary containing success result and a status message
    """
    fields = {
        55: symbol,  # Symbol
        54: side,    # Side (1=Buy, 2=Sell)
        40: ord_type, # OrdType (1=Market, 2=Limit, etc.)
        44: str(price), # Price
        38: str(qty)   # OrderQty
    }
    success = fix_client.send_fix_message("D", fields)
    return {
        "result": "success" if success else "failed",
        "message": "Order sent successfully" if success else "Order failed"
    }

@mcp.tool()
def send_fix_logout() -> Dict[str, Any]:
    """Send a FIX Logout message.
    
    Returns:
        A dictionary containing success result and a status message
    """
    success = fix_client.send_logout()
    return {
        "result": "success" if success else "failed",
        "message": "Logout sent successfully" if success else "Logout failed"
    }

@mcp.tool()
def send_fix_test_request(test_req_id: str) -> Dict[str, Any]:
    """Send a FIX Test Request message.

    Args:
        test_req_id: The test request ID
    
    Returns:
        A dictionary containing success result and a status message
    """
    success = fix_client.send_test_request(test_req_id)
    return {
        "result": "success" if success else "failed",
        "message": "Test request sent successfully" if success else "Test request failed"
    }

@mcp.tool()
def send_fix_resend_request(begin_seq_no: int, end_seq_no: int) -> Dict[str, Any]:
    """Send a FIX Resend Request message.

    Args:
        begin_seq_no: Beging sequence number
        end_seq_no: End sequence number

    Returns:
        A dictionary containing success result and a status message
    """
    success = fix_client.send_resend_request(begin_seq_no, end_seq_no)
    return {
        "result": "success" if success else "failed",
        "message": "Resend request sent successfully" if success else "Resend request failed"
    }

@mcp.tool()
def send_fix_session_reject(ref_seq_no: int, reject_reason: int) -> Dict[str, Any]:
    """Send a FIX Session Level Reject message.

    Args:
        ref_seq_no: MsgSeqNum of rejected message
        reject_reason: Code to identify reason for a session-level Reject message
    
    Returns:
        A dictionary containing success result and a status message
    """
    success = fix_client.send_session_reject(ref_seq_no, reject_reason)
    return {
        "result": "success" if success else "failed",
        "message": "Session reject sent successfully" if success else "Session reject failed"
    }

@mcp.tool()
def send_fix_sequence_reset(new_seq_no: int, gap_fill: bool = False) -> Dict[str, Any]:
    """Send a FIX Sequence Reset (Gap Fill) message.

    Args:
        new_seq_no: New sequence number to reset to
        gap_fill: Gap fill flag
    
    Returns:
        A dictionary containing success result and a status message
    """
    success = fix_client.send_sequence_reset(new_seq_no, gap_fill)
    return {
        "result": "success" if success else "failed",
        "message": "Sequence reset sent successfully" if success else "Sequence reset failed"
    }

@mcp.resource("fix/status")
def get_fix_status() -> Dict[str, Any]:
    """Get the current connection status of the FIX client.
    
    Returns:
        A dictionary containing success result and a status message
    """
    return {
        "result": "success",
        "message": f"Connected: {fix_client.is_connected}, Last Sequence: {fix_client.msg_seq_num}"
    }