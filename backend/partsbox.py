import httpx
import logging

logger = logging.getLogger(__name__)

PARTSBOX_API_BASE = "https://api.partsbox.com/api/1/"

# In-memory cache for storage-id → storage-name
storage_name_cache = {}

async def get_part_location(part_id: str, api_key: str) -> str:
    headers = {
        "Authorization": f"APIKey {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    part_payload = {"part/id": part_id}

    try:
        async with httpx.AsyncClient() as client:
            part_url = PARTSBOX_API_BASE + "part/get"
            logger.info(f"POST {part_url} with part/id: {part_id}")
            part_resp = await client.post(part_url, headers=headers, json=part_payload)
            logger.info(f"Status: {part_resp.status_code}")
            part_resp.raise_for_status()

            part_data = part_resp.json()
            stock_entries = part_data.get("data", {}).get("part/stock", [])
            if not stock_entries:
                logger.info("No stock entries found for part")
                return "No stock"

            # Find a valid stock entry with a positive quantity
            storage_id = None
            for entry in stock_entries:
                if entry.get("stock/quantity", 0) > 0:
                    storage_id = entry.get("stock/storage-id")
                    break

            if not storage_id:
                logger.info("No usable stock with storage ID")
                return "No usable stock"

            # Check cache
            if storage_id in storage_name_cache:
                logger.info(f"Storage name cache hit for {storage_id}")
                return storage_name_cache[storage_id]

            # Call storage/get to resolve name
            storage_payload = {"storage/id": storage_id}
            storage_url = PARTSBOX_API_BASE + "storage/get"
            logger.info(f"POST {storage_url} with storage/id: {storage_id}")
            storage_resp = await client.post(storage_url, headers=headers, json=storage_payload)
            logger.info(f"Storage status: {storage_resp.status_code}")
            storage_resp.raise_for_status()

            storage_data = storage_resp.json()
            name = storage_data.get("data", {}).get("storage/name")

            if not name:
                logger.warning(f"Storage ID {storage_id} resolved, but no name field returned")
                name = storage_id

            # Cache the result
            storage_name_cache[storage_id] = name
            logger.info(f"Resolved storage name: {name}")
            return name

    except Exception as e:
        logger.exception("Error resolving storage location")
        return "Error"
