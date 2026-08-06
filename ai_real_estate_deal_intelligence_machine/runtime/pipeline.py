from ai_real_estate_deal_intelligence_machine.runtime.deal_context import (
    DealContext,
)

from ai_real_estate_deal_intelligence_machine.acquisition.seller_lead_pipeline import (
    SellerLeadPipeline,
)

from ai_real_estate_deal_intelligence_machine.intelligence.deal_intelligence_coordinator import (
    DealIntelligenceCoordinator,
)

from ai_real_estate_deal_intelligence_machine.matching.buyer_matching_engine import (
    BuyerMatchingEngine,
)

from ai_real_estate_deal_intelligence_machine.deal_packaging.deal_package_generator import (
    DealPackageGenerator,
)

from ai_real_estate_deal_intelligence_machine.execution.deal_execution_engine import (
    DealExecutionEngine,
)

from ai_real_estate_deal_intelligence_machine.database.models import (
    DealRecord,
)

from ai_real_estate_deal_intelligence_machine.database.deal_repository import (
    DealRepository,
)


class AutonomousPipeline:
    """
    Autonomous Real Estate Deal Intelligence Pipeline.

    Sprint 4 Part 3 Architecture:

    Seller Intelligence
            |
            v
    Deal Underwriting
            |
            v
    Buyer Intelligence
            |
            v
    Deal Packaging
            |
            v
    Execution Readiness
            |
            v
    Persistent Deal Memory
            |
            v
    Learning System Ready


    """


    def __init__(self):

        self.seller_pipeline = SellerLeadPipeline()

        self.intelligence = DealIntelligenceCoordinator()

        self.buyer_matching = BuyerMatchingEngine()

        self.package_generator = DealPackageGenerator()

        self.execution = DealExecutionEngine()

        self.deal_repository = DealRepository()



    def execute(
        self,
        context: DealContext,
    ):

        print()
        print("=" * 70)
        print("AUTONOMOUS INVESTMENT ANALYSIS STARTED")
        print("=" * 70)



        # ======================================================
        # STEP 1
        # SELLER OPPORTUNITY ANALYSIS
        # ======================================================


        print()
        print("STEP 1 - Seller Opportunity Analysis")


        opportunity = context.opportunity


        seller_results = self.seller_pipeline.analyze_lead(

            market=opportunity.get(
                "market",
                "Unknown"
            ),

            property_address=opportunity.get(
                "property_address",
                "Unknown Address"
            ),

            estimated_value=opportunity.get(
                "estimated_value",
                0
            ),

            motivation_score=opportunity.get(
                "motivation_score",
                0
            ),

            distress_signals=opportunity.get(
                "distress_signals",
                []
            ),

        )


        print(seller_results)



        seller_id = (
            seller_results[0].seller_id
            if seller_results
            else "UNKNOWN"
        )



        # ======================================================
        # STEP 2
        # DEAL INTELLIGENCE
        # ======================================================


        print()
        print("STEP 2 - Deal Intelligence Analysis")


        purchase_price = 150000

        repair_cost = 35000


        intelligence_result = self.intelligence.analyze(

            property_id=context.deal_id,

            purchase_price=purchase_price,

            estimated_value=opportunity.get(
                "estimated_value",
                0
            ),

            repair_cost=repair_cost,

        )


        print(intelligence_result)



        # ======================================================
        # STEP 3
        # BUYER MATCHING
        # ======================================================


        print()
        print("STEP 3 - Buyer Matching")


        buyers = [

            {
                "buyer_id": "BUYER-001",
                "buyer_name": "Detroit Cash Investors",
                "preferred_markets": [
                    "Detroit"
                ],
                "preferred_property_types": [
                    "single_family"
                ],
                "investment_score": 95,
            },


            {
                "buyer_id": "BUYER-002",
                "buyer_name": "Midwest Rental Group",
                "preferred_markets": [
                    "Detroit"
                ],
                "preferred_property_types": [
                    "multi_family"
                ],
                "investment_score": 85,
            },

        ]


        deal = {

            "market":
                opportunity.get(
                    "market",
                    "Unknown"
                ),

            "property_type":
                "single_family",

        }


        buyer_matches = self.buyer_matching.match(

            buyers=buyers,

            deal=deal,

        )


        print(buyer_matches)



        # ======================================================
        # STEP 4
        # DEAL PACKAGE GENERATION
        # ======================================================


        print()
        print("STEP 4 - Deal Package Generation")


        roi_percentage = (

            intelligence_result.projected_profit

            /

            intelligence_result.purchase_price

            *

            100

        )


        underwriting = {


            "property_id":
                intelligence_result.property_id,


            "address":
                opportunity.get(
                    "property_address",
                    "Unknown Address"
                ),


            "arv":
                intelligence_result.estimated_value,


            "purchase_price":
                intelligence_result.purchase_price,


            "repair_cost":
                intelligence_result.repair_cost,


            "projected_profit":
                intelligence_result.projected_profit,


            "roi_percentage":
                roi_percentage,


            "recommendation":
                intelligence_result.recommendation,


            "deal_score":
                intelligence_result.deal_score,


            "risk_level":
                intelligence_result.risk_level,


        }



        buyer_data = []


        for buyer in buyer_matches:

            buyer_data.append(

                {

                    "buyer_id":
                        buyer.buyer_id,

                    "buyer_name":
                        buyer.buyer_name,

                    "score":
                        buyer.score,

                    "recommendation":
                        buyer.recommendation,

                    "reasoning":
                        buyer.reasoning,

                }

            )



        package = self.package_generator.generate(

            underwriting,

            buyer_data,

        )


        print(package)



        # ======================================================
        # STEP 5
        # EXECUTION
        # ======================================================


        print()
        print("STEP 5 - Execution Readiness")


        execution_result = self.execution.execute(

            package

        )


        print(execution_result)



        # ======================================================
        # STEP 6
        # DEAL MEMORY
        # ======================================================


        print()
        print("STEP 6 - Saving Deal Memory")


        deal_record = DealRecord(

            deal_id=context.deal_id,

            property_id=intelligence_result.property_id,

            seller_id=seller_id,

            recommendation=intelligence_result.recommendation,

            deal_score=intelligence_result.deal_score,

            projected_profit=intelligence_result.projected_profit,

            roi=roi_percentage,

            risk_level=intelligence_result.risk_level,

            status="COMPLETED",

        )



        saved_deal = self.deal_repository.save_deal(

            deal_record

        )


        print()
        print("Deal Saved:")
        print(saved_deal)



        print()
        print("=" * 70)
        print("AUTONOMOUS INVESTMENT ANALYSIS COMPLETE")
        print("=" * 70)



        return {


            "deal_id":
                context.deal_id,


            "seller_analysis":
                seller_results,


            "investment_analysis":
                intelligence_result,


            "buyer_matches":
                buyer_matches,


            "deal_package":
                package,


            "execution":
                execution_result,


            "stored_deal":
                saved_deal,


            "recommendation":
                intelligence_result.recommendation,


            "status":
                "COMPLETED",


        }