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


class AutonomousPipeline:
    """
    End-to-end autonomous investment pipeline.

    Flow:

    Seller Opportunity
            |
            v
    Seller Intelligence
            |
            v
    Deal Underwriting
            |
            v
    Buyer Matching
            |
            v
    Investor Package
            |
            v
    Execution Readiness
            |
            v
    Investment Recommendation
    """


    def __init__(self):

        self.seller_pipeline = SellerLeadPipeline()

        self.intelligence = DealIntelligenceCoordinator()

        self.buyer_matching = BuyerMatchingEngine()

        self.package_generator = DealPackageGenerator()

        self.execution = DealExecutionEngine()



    def execute(
        self,
        context: DealContext,
    ):

        print()
        print("=" * 70)
        print(
            "AUTONOMOUS INVESTMENT ANALYSIS STARTED"
        )
        print("=" * 70)



        # =====================================================
        # STEP 1 - SELLER ANALYSIS
        # =====================================================

        print()
        print(
            "STEP 1 - Seller Opportunity Analysis"
        )


        seller_results = self.seller_pipeline.analyze_lead(

            market=context.opportunity["market"],

            property_address=context.opportunity["property_address"],

            estimated_value=context.opportunity["estimated_value"],

            motivation_score=context.opportunity["motivation_score"],

            distress_signals=context.opportunity["distress_signals"],

        )


        print(
            seller_results
        )



        # =====================================================
        # STEP 2 - DEAL INTELLIGENCE
        # =====================================================

        print()
        print(
            "STEP 2 - Deal Intelligence Analysis"
        )


        purchase_price = 150000

        repair_cost = 35000


        intelligence_result = self.intelligence.analyze(

            property_id=context.deal_id,

            purchase_price=purchase_price,

            estimated_value=context.opportunity["estimated_value"],

            repair_cost=repair_cost,

        )


        print(
            intelligence_result
        )



        # =====================================================
        # STEP 3 - BUYER MATCHING
        # =====================================================

        print()
        print(
            "STEP 3 - Buyer Matching"
        )


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
                context.opportunity["market"],

            "property_type":
                "single_family",

        }


        buyer_matches = self.buyer_matching.match(

            buyers=buyers,

            deal=deal,

        )


        print(
            buyer_matches
        )



        # =====================================================
        # STEP 4 - DEAL PACKAGE GENERATION
        # =====================================================

        print()
        print(
            "STEP 4 - Deal Package Generation"
        )


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
                context.opportunity["property_address"],


            "market":
                context.opportunity["market"],


            "deal_score":
                intelligence_result.deal_score,


            "recommendation":
                intelligence_result.recommendation,


            "priority":
                intelligence_result.priority,


            "risk_level":
                intelligence_result.risk_level,


            # Purchase numbers

            "purchase_price":
                intelligence_result.purchase_price,


            "arv":
                intelligence_result.estimated_value,


            "estimated_value":
                intelligence_result.estimated_value,


            "repair_cost":
                intelligence_result.repair_cost,


            "projected_profit":
                intelligence_result.projected_profit,


            "mao":
                intelligence_result.mao,


            "profit_margin":
                intelligence_result.profit_margin,


            "roi_percentage":
                roi_percentage,


            # Additional package fields

            "after_repair_value":
                intelligence_result.estimated_value,


            "total_investment":
                (
                    intelligence_result.purchase_price
                    +
                    intelligence_result.repair_cost
                ),


            "investment_strategy":
                "Fix and Flip / Wholesale Opportunity",


            "exit_strategy":
                "Cash Buyer Assignment or Investor Sale",

        }



        buyer_data = [

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

            for buyer in buyer_matches

        ]



        package = self.package_generator.generate(

            underwriting,

            buyer_data,

        )


        print(
            package
        )



        # =====================================================
        # STEP 5 - EXECUTION
        # =====================================================

        print()

        print(
            "STEP 5 - Execution Readiness"
        )


        execution_result = self.execution.execute(

            package

        )


        print(
            execution_result
        )



        print()

        print("=" * 70)

        print(
            "AUTONOMOUS INVESTMENT ANALYSIS COMPLETE"
        )

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


            "recommendation":
                intelligence_result.recommendation,


            "status":
                "COMPLETED",

        }