# fix-mcp
Financial Information eXchange (FIX) protocol in FastMCP.

This server exposes resources and tools for FIX trading functions mainly focus on FIX v4.2, making it easy to integrate into MCP-compatible clients, including Claude Desktop.

![GitHub](https://img.shields.io/github/license/aliasmaya/fix-mcp) 
![GitHub last commit](https://img.shields.io/github/last-commit/aliasmaya/fix-mcp) 
![Python](https://img.shields.io/badge/python-3.10%2B-blue)

## Features

- **Administrative Messages**: Address the utility needs of the protocol.
- **Application Messages**: To accomplish the exchange business related information with standard header followed by the message body and trailer.

## Installation

Clone the repository:

```bash
git clone https://github.com/aliasmaya/fix-mcp.git
cd fix-mcp
```  

Install for Claude Desktop
```
mcp install main.py --name "fix-protocol"
```
Then enable it in your Claude Desktop configuration.

For other clients, add a server entry to your configuration file:

```
"mcpServers": { 
  "fix-mcp": { 
    "command": "uv", 
    "args": [ 
      "--directory", "/your/path/to/fix-mcp", 
      "run", 
      "main.py" 
    ]
  } 
}
```
