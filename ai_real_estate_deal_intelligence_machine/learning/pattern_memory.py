from __future__ import annotations

from typing import Any, Dict, List


class PatternMemory:
    """
    Stores discovered investment patterns.

    Sprint 4 Part 9:
    Learning Intelligence Integration.

    This module converts historical deal outcomes into
    reusable investment intelligence.
    """

    def __init__(self) -> None:
        self._patterns: List[Dict[str, Any]] = []

    def store(
        self,
        pattern: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Store a discovered investment pattern.
        """

        self._patterns.append(pattern)

        return pattern

    def get_all(self) -> List[Dict[str, Any]]:
        """
        Return all learned patterns.
        """

        return list(self._patterns)

    def find_by_market(
        self,
        market: str,
    ) -> List[Dict[str, Any]]:
        """
        Find patterns matching a market.
        """

        return [
            pattern
            for pattern in self._patterns
            if pattern.get("market") == market
        ]

    def count(self) -> int:
        """
        Return number of learned patterns.
        """

        return len(self._patterns)

    def summary(self) -> Dict[str, Any]:
        """
        Return learning memory summary.
        """

        return {
            "total_patterns": len(self._patterns),
            "markets": list(
                {
                    pattern.get("market")
                    for pattern in self._patterns
                    if pattern.get("market")
                }
            ),
            "status": "PATTERN_MEMORY_READY",
        }