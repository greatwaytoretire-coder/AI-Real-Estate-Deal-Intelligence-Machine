from dataclasses import dataclass


@dataclass
class SellerLead:
    seller_id: str
    owner_name: str
    market: str
    property_address: str
    estimated_value: float
    motivation_score: float
    distress_signals: list[str]


@dataclass
class PrioritizedLead:
    seller_id: str
    owner_name: str
    priority_score: float
    recommendation: str
    reasoning: list[str]


class SellerLeadPipeline:
    """
    Prioritizes motivated seller opportunities.

    Flow:

    Seller Lead
          |
          v
    Motivation Analysis
          |
          v
    Lead Prioritization
    """

    def __init__(self):

        self.leads = [

            SellerLead(
                seller_id="SELLER-001",
                owner_name="John Smith",
                market="Test Market",
                property_address="123 Main Street",
                estimated_value=275000,
                motivation_score=92,
                distress_signals=[
                    "Vacant Property",
                    "Tax Delinquent",
                ],
            ),

            SellerLead(
                seller_id="SELLER-002",
                owner_name="Mary Johnson",
                market="Test Market",
                property_address="456 Oak Avenue",
                estimated_value=425000,
                motivation_score=68,
                distress_signals=[
                    "Inherited Property",
                ],
            ),

        ]


    def analyze_lead(
        self,
        market: str,
        property_address: str,
        estimated_value: float,
        motivation_score: float,
        distress_signals: list[str],
    ) -> list[PrioritizedLead]:
        """
        Analyze a seller lead submitted through the API.
        """

        seller_lead = SellerLead(
            seller_id="API-SELLER-001",
            owner_name="Unknown Owner",
            market=market,
            property_address=property_address,
            estimated_value=estimated_value,
            motivation_score=motivation_score,
            distress_signals=distress_signals,
        )

        score = seller_lead.motivation_score

        reasoning = []


        if seller_lead.motivation_score >= 90:

            reasoning.append(
                "Highly motivated seller."
            )

            recommendation = (
                "Immediate acquisition outreach."
            )


        elif seller_lead.motivation_score >= 75:

            reasoning.append(
                "Strong acquisition opportunity."
            )

            recommendation = (
                "Priority follow-up."
            )


        else:

            reasoning.append(
                "Monitor for future opportunity."
            )

            recommendation = (
                "Nurture campaign."
            )


        if len(seller_lead.distress_signals) >= 2:

            score += 5

            reasoning.append(
                "Multiple distress indicators detected."
            )


        return [

            PrioritizedLead(
                seller_id=seller_lead.seller_id,
                owner_name=seller_lead.owner_name,
                priority_score=score,
                recommendation=recommendation,
                reasoning=reasoning,
            )

        ]


    def prioritize_leads(self) -> list[PrioritizedLead]:

        prioritized = []


        for lead in self.leads:

            score = lead.motivation_score

            reasoning = []


            if lead.motivation_score >= 90:

                reasoning.append(
                    "Highly motivated seller."
                )

                recommendation = (
                    "Immediate acquisition outreach."
                )


            elif lead.motivation_score >= 75:

                reasoning.append(
                    "Strong acquisition opportunity."
                )

                recommendation = (
                    "Priority follow-up."
                )


            else:

                reasoning.append(
                    "Monitor for future opportunity."
                )

                recommendation = (
                    "Nurture campaign."
                )


            if len(lead.distress_signals) >= 2:

                score += 5

                reasoning.append(
                    "Multiple distress indicators detected."
                )


            prioritized.append(

                PrioritizedLead(
                    seller_id=lead.seller_id,
                    owner_name=lead.owner_name,
                    priority_score=score,
                    recommendation=recommendation,
                    reasoning=reasoning,
                )

            )


        return sorted(
            prioritized,
            key=lambda x: x.priority_score,
            reverse=True,
        )