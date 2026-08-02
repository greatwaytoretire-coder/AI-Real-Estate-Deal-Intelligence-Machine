from dataclasses import dataclass


@dataclass
class BuyerProfile:

    buyer_id: str

    name: str

    market: str

    property_types: list[str]

    max_purchase_price: float

    preferred_strategy: str



@dataclass
class BuyerMatch:

    buyer_id: str

    buyer_name: str

    match_score: float

    reasoning: list[str]



class BuyerIntelligenceEngine:
    """
    Matches investment opportunities with qualified buyers.

    Flow:

    Deal Package
          |
          v
    Buyer Profile Analysis
          |
          v
    Match Ranking
    """


    def __init__(self):

        self.buyers = [

            BuyerProfile(
                buyer_id="BUYER-001",
                name="Cash Investor Group",
                market="Test Market",
                property_types=[
                    "single_family",
                    "fix_and_flip",
                ],
                max_purchase_price=500000,
                preferred_strategy="flip",
            ),

            BuyerProfile(
                buyer_id="BUYER-002",
                name="Rental Portfolio Investor",
                market="Test Market",
                property_types=[
                    "single_family",
                ],
                max_purchase_price=750000,
                preferred_strategy="hold",
            ),

        ]


    def find_matches(
        self,
        property_id: str,
        purchase_price: float,
        estimated_value: float,
        repair_cost: float,
    ) -> list[BuyerMatch]:

        matches = []


        projected_profit = (
            estimated_value
            -
            purchase_price
            -
            repair_cost
        )


        for buyer in self.buyers:

            score = 50.0

            reasoning = []


            if purchase_price <= buyer.max_purchase_price:

                score += 25

                reasoning.append(
                    "Purchase price fits buyer criteria."
                )


            if projected_profit > 50000:

                score += 25

                reasoning.append(
                    "Strong projected profit opportunity."
                )


            else:

                reasoning.append(
                    "Profit margin requires review."
                )


            matches.append(

                BuyerMatch(
                    buyer_id=buyer.buyer_id,
                    buyer_name=buyer.name,
                    match_score=score,
                    reasoning=reasoning,
                )

            )


        return sorted(
            matches,
            key=lambda x: x.match_score,
            reverse=True,
        )