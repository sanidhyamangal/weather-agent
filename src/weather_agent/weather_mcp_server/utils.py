import logging
import os
import typing as t

import httpx

logger = logging.getLogger(__name__)


async def make_nws_request(url: str) -> dict[str, t.Any] | None:
    """Make a request to the NWS API with proper error handling."""

    headers = {
        "User-Agent": os.getenv("USER_AGENT"),
        "Accept": "application/geo+json",
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url=url, timeout=30.0, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception:
            logger.error("Error making NWS request", exc_info=True)
            return None


def format_nws_alert(feature: dict) -> str:
    """format the NWS alert for the news data"""

    props = feature["properties"]

    return f"""
Event: {props.get('event', 'Unknown')},
Area: {props.get('areaDesc', 'Unknown')},
Severity: {props.get('severity', 'Unknown')},
Description: {props.get('description', 'No information available')}
Instructions: {props.get('instructions', 'No instructions available')}
"""
