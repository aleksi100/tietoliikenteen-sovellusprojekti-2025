import asyncio
import logging
from typing import Any
from bleak import BleakScanner, BleakClient
from bleak.backends.device import BLEDevice
from bleak.backends.characteristic import BleakGATTCharacteristic
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Asetukset ---
DEVICE_NAME = "kehityslankku"
NOTIFY_CHARACTERISTIC_UUID = "00001526-1212-EFDE-1523-785FEABCD123"

# Tietokanta-asetukset .env-tiedostosta
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "autocommit": True,
    "charset": "utf8mb4",
    "connect_timeout": 10
}

def insert_to_db(groupid: int, from_mac: str, to_mac: str,
                 a: float, b: float, c: float, d: float,
                 e: float = 0.0, f: str = "0"):
    """Avaa uuden yhteyden, lisää rivi ja sulkee yhteyden."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        sql = """
            INSERT INTO rawdata
            (groupid, from_mac, to_mac, sensorvalue_a, sensorvalue_b,
             sensorvalue_c, sensorvalue_d, sensorvalue_e, sensorvalue_f)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (groupid, from_mac, to_mac, a, b, c, d, e, f)
        cursor.execute(sql, values)
        logger.info("Rivi lisätty rawdata-tauluun")
        cursor.close()
        conn.close()
    except Error as e:
        logger.error(f"Tietokantavirhe: {e}")

# --- BLE-osio ---
async def find_device(name: str) -> BLEDevice | None:
    logger.info(f"Etsitään laitetta: {name}")
    devices = await BleakScanner.discover(timeout=10.0)
    for dev in devices:
        if dev.name and name.lower() in dev.name.lower():
            logger.info(f"Löydetty: {dev.name} ({dev.address})")
            return dev
    logger.warning("Laitetta ei löytynyt")
    return None

async def main():
    device = await find_device(DEVICE_NAME)
    if not device:
        return

    async with BleakClient(device, timeout=20.0) as client:
        logger.info("BLE-yhteys muodostettu")

        def notification_handler(char: BleakGATTCharacteristic, data: bytearray):
            try:
                text = data.decode("utf-8").strip()
                logger.info(f"Saapui data: {text}")

                parts = text.split()
                if len(parts) >= 4:
                    a = float(parts[0])
                    b = float(parts[1])
                    c = float(parts[2])
                    d = float(parts[3])

                    insert_to_db(
                        groupid=22,
                        from_mac="AA:BB:CC:DD:EE:FF",
                        to_mac="11:22:33:44:55:66",
                        a=a, b=b, c=c, d=d,
                        e=0.0,
                        f="OK"
                    )
            except Exception as e:
                logger.error(f"Viestin käsittely epäonnistui: {e}")

        try:
            await client.start_notify(NOTIFY_CHARACTERISTIC_UUID, notification_handler)
            logger.info("Ilmoitukset aktivoitu – kuunellaan dataa...")
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("Käyttäjä lopetti")
        except Exception as e:
            logger.error(f"Bleak-virhe: {e}")
        finally:
            await client.stop_notify(NOTIFY_CHARACTERISTIC_UUID)

if __name__ == "__main__":
    asyncio.run(main())
