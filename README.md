# pyBittle-mcp-server

A Python MCP (Model Context Protocol) server for controlling the Bittle robot via Bluetooth. This server exposes a set of commands to move, pose, and interact with Bittle using the MCP protocol.

## Features

- Connects to Bittle via Bluetooth
- Exposes movement and pose commands (forward, backward, turn, sit, rest, etc.)
- Integrates with MCP tools for remote and programmatic control
- Logs all activity to `bittle_mcp.log`

## Requirements

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) for package management
- Bittle robot with Bluetooth enabled
- [pyBittle](https://github.com/cluesang/pyBittle) library
- [mcp-server](https://github.com/cluesang/pyBittle-mcp-server) library

## Installation & Setup

1. **Install uv (recommended for fast, reliable Python package management):**
   ```bash
   curl -Ls https://astral.sh/uv/install.sh | sh
   ```

2. **Install uvx (required for MCP server):**
   ```bash
   curl -Ls https://astral.sh/uvx/install.sh | sh
   ```

3. **Install dependencies:**
   ```bash
   # Option 1: Using start_server.sh (recommended)
   chmod +x start_server.sh
   ./start_server.sh

   # Option 2: Manual installation
   uv pip install -r requirements.txt
   # or, if using pyproject.toml:
   uv pip install -r pyproject.toml
   ```

## Usage

1. **Configure Bluetooth:**
   Ensure your Bittle robot is powered on and in Bluetooth pairing mode.

2. **Run the MCP server:**
   ```bash
   # Option 1: Using start_server.sh (recommended)
   ./start_server.sh
   
   # Option 2: Manual start
   uvx mcpo --port 8080 -- uv run --with 'mcp[cli]' --with git+https://github.com/cluesang/pyBittle.git mcp run ./server.py
   ```
   The server will attempt to connect to Bittle and log status to `bittle_mcp.log`.

3. **Integrate with MCP tools:**
   - This server exposes commands via the MCP protocol, making them accessible to any MCP-compatible client or tool.
   - You can use the [MCP CLI](https://github.com/modelcontext/mcp-cli) or other MCP tools to discover and invoke available commands on your Bittle robot.
   - Example (using MCP CLI):
     ```bash
     mcp call move_forward
     mcp call sit
     mcp call rest
     ```
   - All available commands are decorated with `@mcp.tool()` in `server.py` and are automatically registered with the MCP server.

## Development

- The main logic is in `server.py`.
- Logging is configured to output to both console and `bittle_mcp.log`.
- Commands are decorated with `@mcp.tool()` for MCP exposure.
- Use `start_server.sh` for development as it handles environment setup and process management.

## Troubleshooting

- If the server fails to connect, check Bluetooth pairing and ensure no other process is using the Bittle connection.
- Review `bittle_mcp.log` for detailed error messages.
- If you encounter port conflicts, `start_server.sh` will automatically handle killing existing server processes.
- Make sure both `uv` and `uvx` are installed and available in your PATH.

## License

MIT License
