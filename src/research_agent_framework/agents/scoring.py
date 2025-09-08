from typing import Any, Dict

from research_agent_framework.models import SerpResult, Location, Rating


class SimpleScorer:
    """Example scoring implementation used in tests and notebooks.

    Rules (example, deterministic):
    - Base score starts at 0.0
    - If `rating.score` exists, add (rating.score / 5) * 0.6
    - If `location.distance` exists and is numeric or pint.Quantity, add a distance-based bonus up to 0.3
    - If `price_level` is FREE/CHEAP, add 0.05; EXPENSIVE subtracts 0.05
    - Clamp final score to [0.0, 1.0]
    """

    def _distance_bonus(self, loc: Location) -> float:
        d = loc.distance
        if d is None:
            return 0.0
        # Handle pint.Quantity or numeric
        try:
            # pint.Quantity has .magnitude
            mag = getattr(d, "magnitude", None)
            if mag is not None:
                meters = float(mag)
            else:
                meters = float(d)
        except Exception:
            return 0.0
        # Closer is better: score contribution decreases with distance up to 5000m
        if meters <= 0:
            return 0.15
        ratio = max(0.0, min(1.0, 1.0 - (meters / 5000.0)))
        return 0.15 * ratio

    def score(self, item: Any, preferences: Dict[str, Any] | None = None) -> Dict[str, Any]:
        base = 0.0
        reason_parts = []

        loc = None
        if isinstance(item, SerpResult):
            loc = item.location
            rating = item.rating
            price = getattr(item, "price_level", None)
        elif isinstance(item, Location):
            loc = item
            rating = None
            price = None
        else:
            # attempt duck typing
            loc = getattr(item, "location", None) or (item if isinstance(item, Location) else None)
            rating = getattr(item, "rating", None)
            price = getattr(item, "price_level", None)

        # rating contribution
        r_raw = getattr(rating, "score", None)
        if r_raw is not None:
            try:
                r = float(r_raw)
                contrib = (r / 5.0) * 0.6
                base += contrib
                reason_parts.append(f"rating:{r:.2f}->{contrib:.3f}")
            except Exception:
                pass

        # distance contribution
        if loc is not None:
            db = self._distance_bonus(loc)
            base += db
            if db:
                reason_parts.append(f"distance_bonus:{db:.3f}")

        # price contribution
        if price is not None:
            try:
                p = str(price).lower()
                if p in ("free", "cheap"):
                    base += 0.05
                    reason_parts.append("price:cheap+0.05")
                elif p == "expensive":
                    base -= 0.05
                    reason_parts.append("price:expensive-0.05")
            except Exception:
                pass

        # preference override (optional)
        if preferences and "weight" in preferences:
            try:
                w = float(preferences["weight"])
                base = max(0.0, min(1.0, base * w))
                reason_parts.append(f"pref_weight:{w}")
            except Exception:
                pass

        final = max(0.0, min(1.0, base))
        return {"score": float(final), "reason": ";".join(reason_parts), "meta": {"raw_base": base}}
