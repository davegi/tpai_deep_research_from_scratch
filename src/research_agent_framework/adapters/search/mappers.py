from typing import Dict, Any, Tuple, Optional


def _extract_coords(item: Dict[str, Any]) -> Optional[Tuple[float, float]]:
    """Try several common keys to extract (lat, lon) coordinates."""
    lat_keys = ("lat", "latitude", "gps_lat", "point_lat")
    lon_keys = ("lon", "lng", "longitude", "gps_lon", "point_lng")
    lat = None
    lon = None
    for k in lat_keys:
        if k in item:
            try:
                lat = float(item[k])
                break
            except Exception:
                pass
    for k in lon_keys:
        if k in item:
            try:
                lon = float(item[k])
                break
            except Exception:
                pass
    if lat is not None and lon is not None:
        return lat, lon
    # Some providers nest coords
    if "geometry" in item and isinstance(item["geometry"], dict):
        g = item["geometry"]
        # GeoJSON style
        coords = g.get("coordinates")
        if isinstance(coords, (list, tuple)) and len(coords) >= 2:
            try:
                return float(coords[1]), float(coords[0])
            except Exception:
                pass
    return None


def map_serpapi_item(item: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize SerpAPI-like item payloads into a common shape.

    This maps common aliases and extracts structured pieces likely to be present across provider responses.
    """
    normalized: Dict[str, Any] = dict(item)

    # URL fields
    if "link" in item and "url" not in item:
        normalized["url"] = item["link"]
    if "unescapedUrl" in item and "url" not in normalized:
        normalized["url"] = item["unescapedUrl"]

    # Title/name
    if "title" not in normalized:
        for alt in ("name", "heading", "titleNoFormatting"):
            if alt in item:
                normalized["title"] = item[alt]
                break

    # Snippet/description
    for alt in ("snippet", "snippet_text", "description", "summary"):
        if alt in item and "snippet" not in normalized:
            normalized["snippet"] = item[alt]
            break

    # Address / phone
    if "formatted_address" in item and "address" not in normalized:
        normalized["address"] = item["formatted_address"]
    if "phone" in item and "phone" not in normalized:
        normalized["phone"] = item["phone"]

    # Ratings / reviews
    if "rating" in item:
        normalized.setdefault("rating", item.get("rating"))
    if "reviews_count" in item:
        normalized.setdefault("reviews_count", item.get("reviews_count"))
    if "user_ratings_total" in item:
        normalized.setdefault("reviews_count", item.get("user_ratings_total"))

    # Price / category
    for pk in ("price", "price_level", "price_range"):
        if pk in item and "price" not in normalized:
            normalized["price"] = item[pk]
            break
    if "category" in item and "categories" not in normalized:
        normalized["categories"] = item["category"]
    if "types" in item and "categories" not in normalized:
        normalized["categories"] = item["types"]

    # Images
    if "thumbnail" in item and "image" not in normalized:
        normalized["image"] = item["thumbnail"]
    if "image" not in normalized and "image_url" in item:
        normalized["image"] = item["image_url"]

    # IDs
    for idk in ("id", "place_id", "cid", "result_id"):
        if idk in item and "id" not in normalized:
            normalized["id"] = item[idk]
            break

    # Coordinates
    coords = _extract_coords(item)
    if coords:
        normalized.setdefault("latlon", {"lat": coords[0], "lon": coords[1]})

    return normalized


def map_tavily_item(item: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize Tavily-like item payloads into a common shape.

    Tavily responses commonly use `href`, `name`, `summary`, `location`, etc.
    """
    normalized: Dict[str, Any] = dict(item)

    # URL
    if "href" in item and "url" not in normalized:
        normalized["url"] = item["href"]
    if "link" in item and "url" not in normalized:
        normalized["url"] = item["link"]

    # Title / name
    if "title" not in normalized and "name" in item:
        normalized["title"] = item["name"]

    # Snippet / summary
    if "snippet" not in normalized and "summary" in item:
        normalized["snippet"] = item["summary"]

    # Address and phone in a nested `location` or `contact`
    if "location" in item and isinstance(item["location"], dict):
        loc = item["location"]
        if "address" in loc and "address" not in normalized:
            normalized["address"] = loc["address"]
        c = loc.get("coords") or loc.get("coordinate") or loc.get("latlng")
        if isinstance(c, dict):
            lat = c.get("lat") or c.get("latitude")
            lon = c.get("lon") or c.get("lng") or c.get("longitude")
            if lat and lon:
                try:
                    normalized.setdefault("latlon", {"lat": float(lat), "lon": float(lon)})
                except Exception:
                    pass

    # rating/reviews
    if "rating" in item:
        normalized.setdefault("rating", item.get("rating"))
    if "reviews" in item and isinstance(item["reviews"], (int, float)):
        normalized.setdefault("reviews_count", item.get("reviews"))

    # categories / tags
    if "tags" in item and "categories" not in normalized:
        normalized["categories"] = item["tags"]

    # images
    if "images" in item and "image" not in normalized:
        imgs = item.get("images")
        if isinstance(imgs, (list, tuple)) and imgs:
            normalized["image"] = imgs[0]

    # ids
    if "id" in item and "id" not in normalized:
        normalized["id"] = item["id"]

    return normalized


def map_generic_item(item: Dict[str, Any]) -> Dict[str, Any]:
    """Fallback mapper that copies the incoming dict. Providers should add
    their own mappers for better coverage.
    """
    return dict(item)
