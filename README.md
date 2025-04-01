# FIX-MCP: FIX Protocol 4.2 Buy-Side Client with Model Context Protocol

Welcome to the FIX-MCP project! This Python-based implementation provides a buy-side client for the Financial Information eXchange (FIX) Protocol version 4.2, integrated with the Model Context Protocol (MCP) using the FastMCP library. It enables seamless interaction between large language models (LLMs) and FIX systems, supporting administrative messages, order management, and reconnectable TCP/IP sockets.

![GitHub](https://img.shields.io/github/license/aliasmaya/fix-mcp) 
![GitHub last commit](https://img.shields.io/github/last-commit/aliasmaya/fix-mcp) 
![Python](https://img.shields.io/badge/python-3.10%2B-blue)

## Overview

The FIX-MCP project acts as a bridge between financial systems using FIX 4.2 and modern AI-driven applications via MCP. It is designed as a buy-side client that connects to a sell-side FIX server, handles session management, and exposes FIX functionality (e.g., orders, heartbeats, logouts) as MCP tools and resources. This allows LLMs or other clients to interact with FIX systems programmatically.

## Highlight Features

- **FIX Protocol 4.2 Support**: Implements core FIX messages including New Order Single, Execution Report, Logon, Logout, Heartbeat, Test Request, Resend Request, Session Level Reject, and Sequence Reset (Gap Fill).

- **Model Context Protocol (MCP) Integration**: Uses FastMCP to expose FIX functionality as tools and resources, enabling LLMs to call FIX operations like sending orders or managing sessions.

- **Reconnectable TCP/IP Socket**: Ensures robust connectivity with automatic reconnection logic, handling network failures gracefully with up to 5 retry attempts and exponential backoff.

- **Administrative Message Support**: Full support for session-level messages (Logon, Logout, Heartbeat, Test Request, Resend Request, Session Level Reject, Sequence Reset) to maintain and manage FIX sessions.

- **Order Execution Tracking**: Waits for and processes Execution Reports to determine if New Single Orders are successful, providing detailed feedback (e.g., Filled, Rejected).

- **Logging and Error Handling**: Includes comprehensive logging and error handling for debugging and reliability.

- **Scalable Design**: Built with Python's standard library and FastMCP, making it easy to extend or integrate into larger systems.

## Installation

To get started with FIX-MCP, clone this repository and install the required dependencies:

```bash
git clone https://github.com/aliasmaya/fix-mcp.git
cd fix-mcp
pip install fastmcp
```

### Prerequisites

- Python 3.10 or higher
- A running FIX sell-side server (for testing, adjust the `SELLSIDE_HOST` and `SELLSIDE_PORT` in `.env` to match your server)

## Usage

### Running the Server

1. Ensure your FIX sell-side server is running (e.g., at `localhost:5000`).
2. Run the MCP server:

```bash
python main.py
```

The server will start and listen for MCP requests, exposing FIX tools and resources. You can interact with it using an LLM or a FastMCP client.

### Configuration

1. Copy a `.env` from `.env.example`

```base
cp .env.example .env
```

2. Edit `.env` accordingly:

```ini
SELLSIDE_HOST=localhost
SELLSIDE_PORT=5000
SENDER_COMP_ID=Sender
TARGET_COMP_ID=Target
```

## Contributing

We welcome contributions! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a clear description of your changes.

Please ensure your code follows PEP 8 style guidelines and includes tests if applicable.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the FastMCP team (https://github.com/jlowin/fastmcp) for their MCP implementation.
- Based on FIX Protocol 4.2 specifications (https://www.fixtrading.org/standards/fix-4-2/).

Happy trading and coding!
