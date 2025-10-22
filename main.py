from fastapi import FastAPI
from pydantic import BaseModel
import meshtastic
import meshtastic.serial_interface
from typing import Dict, Any
import os
import logging

# Initialize FastAPI
app = FastAPI(title="Meshtastic FastAPI (configurable SERIAL_PORT)")

# Initialize Meshtastic serial interface (defer/guard by env var)
SERIAL_PORT = os.getenv("SERIAL_PORT", "").strip().lower()  # e.g. "COM7" or "none"
interface = None
if SERIAL_PORT and SERIAL_PORT != "none":
    try:
        logging.info("Attempting to open Meshtastic on %s", SERIAL_PORT)
        interface = meshtastic.serial_interface.SerialInterface(SERIAL_PORT)
    except Exception as e:
        interface = None
        logging.warning("⚠️ Failed to connect to Meshtastic device on %s: %s", SERIAL_PORT, e)
else:
    logging.info("SERIAL_PORT not set or set to 'none' — Meshtastic interface disabled")

# ---- Models ----
class TextMessage(BaseModel):
    destination: str = "^all"  # default broadcast
    text: str

# ---- Routes ----

@app.get("/")
def root():
    """Root endpoint for checking API status"""
    return {"message": "Meshtastic FastAPI is running (serial disabled if SERIAL_PORT not set)"}

@app.get("/nodes")
def get_nodes():
    """Get all nodes in the mesh network"""
    if not interface:
        return {"error": "Device not connected on COM7"}
    
    nodes: Dict[str, Any] = interface.nodes
    node_list = []
    for node_id, node in nodes.items():
        user_info = node.get("user", {})
        metrics = node.get("deviceMetrics", {})
        node_list.append({
            "id": node_id,
            "longName": user_info.get("longName"),
            "shortName": user_info.get("shortName"),
            "lastHeard": node.get("lastHeard"),
            "batteryLevel": metrics.get("batteryLevel"),
        })
    return {"nodes": node_list}

@app.post("/send/text")
def send_text(msg: TextMessage):
    """Send a text message to a node or broadcast"""
    if not interface:
        return {"error": "Device not connected on COM7"}
    
    try:
        interface.sendText(msg.text, destinationId=msg.destination)
        return {"status": "Message sent ✅", "to": msg.destination, "text": msg.text}
    except Exception as e:
        return {"error": str(e)}

@app.get("/device/info")
def device_info():
    """Get connected device information"""
    if not interface:
        return {"error": "Device not connected on COM7"}
    try:
        info = interface.getMyNodeInfo()
        return {"deviceInfo": info}
    except Exception as e:
        return {"error": str(e)}

@app.get("/channels")
def get_channels():
    """Get channel configuration"""
    if not interface:
        return {"error": "Device not connected on COM7"}
    try:
        chans = interface.channels
        return {"channels": chans}
    except Exception as e:
        return {"error": str(e)}