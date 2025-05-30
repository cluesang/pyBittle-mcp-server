import logging
import asyncio
from pyBittle import Bittle, bittleManager
from mcp.server.fastmcp import Context, FastMCP
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pyBittle-MCP")

# Update logging to write to a log file
file_handler = logging.FileHandler("bittle_mcp.log")
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Global variable to track connection status
isConnected = False

# Initialize Bluetooth connection with Bittle
logger.info("Initializing Bluetooth connection with Bittle...")
bittle = Bittle()

async def connect_to_bittle():
    """Establish a Bluetooth connection with the Bittle robot."""
    global isConnected
    try:
        logger.info("Attempting to connect to Bittle...")
        # Initialize Bluetooth first
        # await bittle.bluetoothManager.initialize_name_and_address()
        # Then connect
        await bittle.connect_bluetooth()
        await bittle.receive_msg_bluetooth(log_bluetooth_message)  # Await the coroutine
        await bittle.send_command_bluetooth(bittleManager.Command.REST)
        isConnected = True
        logger.info("Successfully connected to Bittle.")
    except Exception as e:
        isConnected = False
        logger.error(f"Failed to connect to Bittle: {e}")
        raise  # Re-raise the exception to be handled by the caller

@dataclass
class AppContext:
    is_connected: bool = False

@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Manage application lifecycle with type-safe context"""
    # Initialize on startup
    global isConnected 
    try:
        isConnected = await connect_to_bittle()
        yield AppContext(is_connected=isConnected)
    except Exception as e:
        logger.error(f"Error during app startup: {e}")
    finally:
        # Cleanup on shutdown
        pass
        # await cleanup()


# Initialize MCP server
mcp = FastMCP("Bittle", lifespan=app_lifespan)

# Callback function to log received Bluetooth messages
def log_bluetooth_message(device:str, message: str):
    """Log received Bluetooth messages."""
    logger.info(f"Received Bluetooth message: {device} {message}")

# Wrapper to check connection status
def ensure_connected(func):
    async def wrapper(*args, **kwargs):
        if not isConnected:
            logger.error("Bittle is not connected. Please connect before using this command.")
            return
        return await func(*args, **kwargs)
    return wrapper

@ensure_connected
@mcp.tool()
async def move_forward():
    """Command Bittle to move forward."""
    logger.info("Executing move_forward command.")
    await bittle.send_command_bluetooth(bittleManager.Command.FORWARD)
    return "Successfully commanded Bittle to move forward"

@ensure_connected
@mcp.tool()
async def move_backward():
    """Command Bittle to move backward."""
    logger.info("Executing move_backward command.")
    await bittle.send_command_bluetooth(bittleManager.Command.BACKWARD)
    return "Successfully commanded Bittle to move backward"

@ensure_connected
@mcp.tool()
async def turn_left():
    """Command Bittle to turn left."""
    logger.info("Executing turn_left command.")
    await bittle.send_command_bluetooth(bittleManager.Command.LEFT)
    return "Successfully commanded Bittle to turn left"

@ensure_connected
@mcp.tool()
async def turn_right():
    """Command Bittle to turn right."""
    logger.info("Executing turn_right command.")
    await bittle.send_command_bluetooth(bittleManager.Command.RIGHT)
    return "Successfully commanded Bittle to turn right"

@ensure_connected
@mcp.tool()
async def stop():
    """Command Bittle to stop all movement."""
    logger.info("Executing stop command.")
    await bittle.send_command_bluetooth(bittleManager.Command.REST)
    return "Successfully commanded Bittle to stop"

@ensure_connected
@mcp.tool()
async def sit():
    """Command Bittle to sit."""
    logger.info("Executing sit command.")
    await bittle.send_command_bluetooth(bittleManager.Command.SIT)
    return "Successfully commanded Bittle to sit"

@ensure_connected
@mcp.tool()
async def balance():
    """Command Bittle to balance."""
    logger.info("Executing balance command.")
    await bittle.send_command_bluetooth(bittleManager.Command.BALANCE)
    return "Successfully commanded Bittle to balance"

@ensure_connected
@mcp.tool()
async def stretch():
    """Command Bittle to stretch."""
    logger.info("Executing stretch command.")
    await bittle.send_command_bluetooth(bittleManager.Command.STRETCH)
    return "Successfully commanded Bittle to stretch"

@ensure_connected
@mcp.tool()
async def backflip():
    """Command Bittle to perform a backflip."""
    logger.info("Executing backflip command.")
    await bittle.send_command_bluetooth(bittleManager.Command.BACKFLIP)
    return "Successfully commanded Bittle to perform a backflip"

@ensure_connected
@mcp.tool()
async def rest():
    """Command Bittle to rest."""
    logger.info("Executing rest command.")
    await bittle.send_command_bluetooth(bittleManager.Command.REST)
    return "Successfully commanded Bittle to rest"

# Ensure proper cleanup
async def cleanup():
    logger.info("Cleaning up Bluetooth connection...")
    await bittle.disconnect_bluetooth()

# Main function
async def main():
    try:
        # Connect to Bittle
        await connect_to_bittle()
        await asyncio.sleep(5)
        await sit()
        await asyncio.sleep(5)
        await stretch()
        await asyncio.sleep(5)
        await balance()
        await asyncio.sleep(5)
        await rest()

        # Keep the script running until interrupted
        logger.info("Press Ctrl+C to stop the server.")
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        logger.info("Task was cancelled. Cleaning up...")
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt received. Cleaning up...")
    finally:
        await cleanup()


if __name__ == "__main__":
    asyncio.run(main())
else:
    pass
    # If this module is imported, connect to bittle since the mcp servers will be running.
    # asyncio.run(connect_to_bittle())
