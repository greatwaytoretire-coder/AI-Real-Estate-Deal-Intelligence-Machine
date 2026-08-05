from __future__ import annotations

from typing import Any, Dict, List

from .deal_package_models import DealPackage


class DealPackageGenerator:
    """
    Generates an investor-ready deal package.

    Future versions will export PDF reports,
    investor presentations,
    CRM packages,
    and email-ready summaries.
    """

    def generate(
        self,
        underwriting: Dict[str, Any],
        buyer_matches: List[Dict[str, Any]],
    ) -> DealPackage:

        recommendations = [
            buyer["buyer_name"]
            for buyer in buyer_matches
        ]

        summary = (
            f"Projected Profit: ${underwriting['projected_profit']:,.0f} | "
            f"ROI: {underwriting['roi_percentage']:.2f}% | "
            f"Recommendation: {underwriting['recommendation']}"
        )

        return DealPackage(
            property_id=underwriting["property_id"],
            address=underwriting["address"],
            purchase_price=underwriting["purchase_price"],
            arv=underwriting["arv"],
            projected_profit=underwriting["projected_profit"],
            roi=underwriting["roi_percentage"],
            recommendation=underwriting["recommendation"],
            buyer_recommendations=recommendations,
            summary=summary,
        )