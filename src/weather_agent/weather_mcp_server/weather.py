import os

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from weather_agent.weather_mcp_server.utils import format_nws_alert, make_nws_request

load_dotenv()

NWS_API_BASE = os.getenv("NWS_API_BASE")
mcp = FastMCP(
    name="Weather Agent",
)


@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state

    Args:
        state (str): A US state, eg. TN, KY, CA
    """

    url = f"{NWS_API_BASE}/alerts/active?area={state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return f"Unable to fetch any alerts or no alerts for the state: {state}"

    if not data["features"]:
        return f"No active alerts for this state: {state}"

    alerts = [format_nws_alert(feature) for feature in data["features"]]

    return "\n--\n".join(alerts)


@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a given latitude and longitude for the next 5 periods

    Args:
        latitude (float): latitde of the location
        longitude (float): longitude of the location
    """

    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return f"Unable to fetch forecast data for the coordinates: {latitude}, {longitude}"

    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "Unable to fetch detailed forecast"

    periods = forecast_data["properties"]["periods"]
    if not periods:
        return (
            f"No forecast data available for the coordinates: {latitude}, {longitude}"
        )

    forecasts = []
    for period in periods[:5]:
        forecast = f"""
  {period['name']}:
  Temperature: {period['temperature']}{period['temperatureUnit']}
  Wind: {period['windSpeed']}{period['windDirection']}
  Forecast: {period['detailedForecast']}
  """

        forecasts.append(forecast)

    return "\n--\n".join(forecasts)


if __name__ == "__main__":
    mcp.run(transport="sse")
