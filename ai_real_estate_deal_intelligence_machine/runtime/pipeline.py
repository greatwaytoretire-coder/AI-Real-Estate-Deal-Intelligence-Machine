from datetime import datetime, timezone


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


from ai_real_estate_deal_intelligence_machine.learning.learning_models import (
    LearningRecord,
)


from ai_real_estate_deal_intelligence_machine.learning.learning_repository import (
    LearningRepository,
)


from ai_real_estate_deal_intelligence_machine.learning.pattern_detector import (
    PatternDetector,
)



class AutonomousPipeline:
    """
    End-to-end autonomous investment pipeline.

    Sprint 4 Part 3 Upgrade:

    Adds learning intelligence.

    Flow:

    Seller Analysis
          |
          v
    Deal Intelligence
          |
          v
    Buyer Matching
          |
          v
    Deal Package
          |
          v
    Execution
          |
          v
    Deal Memory
          |
          v
    Learning Engine
          |
          v
    Pattern Detection
    """



    def __init__(self):

        self.seller_pipeline = SellerLeadPipeline()

        self.intelligence = DealIntelligenceCoordinator()

        self.buyer_matching = BuyerMatchingEngine()

        self.package_generator = DealPackageGenerator()

        self.execution = DealExecutionEngine()


        self.deal_repository = DealRepository()


        #
        # Sprint 4 Part 3 Learning Layer
        #

        self.learning_repository = LearningRepository()

        self.pattern_detector = PatternDetector()



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


        print(seller_results)



        print()

        print(
            "STEP 2 - Deal Intelligence Analysis"
        )


        intelligence_result = self.intelligence.analyze(

            property_id=context.deal_id,

            purchase_price=150000,

            estimated_value=context.opportunity["estimated_value"],

            repair_cost=35000,

        )


        print(intelligence_result)



        print()

        print(
            "STEP 3 - Buyer Matching"
        )


        buyers = [

            {
                "buyer_id": "BUYER-001",
                "buyer_name": "Detroit Cash Investors",
                "preferred_markets": ["Detroit"],
                "preferred_property_types": ["single_family"],
                "investment_score": 95,
            },

            {
                "buyer_id": "BUYER-002",
                "buyer_name": "Midwest Rental Group",
                "preferred_markets": ["Detroit"],
                "preferred_property_types": ["multi_family"],
                "investment_score": 85,
            },

        ]


        buyer_matches = self.buyer_matching.match(

            buyers=buyers,

            deal={

                "market": context.opportunity["market"],

                "property_type": "single_family",

            },

        )


        print(buyer_matches)



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



        print()

        print(
            "STEP 5 - Execution Readiness"
        )


        execution_result = self.execution.execute(

            package

        )


        print(execution_result)



        print()

        print(
            "STEP 6 - Saving Deal Memory"
        )


        deal_record = DealRecord(

            deal_id=context.deal_id,

            property_id=intelligence_result.property_id,

            seller_id=seller_results[0].seller_id,

            recommendation=intelligence_result.recommendation,

            deal_score=intelligence_result.deal_score,

            projected_profit=intelligence_result.projected_profit,

            roi=roi_percentage,

            risk_level=intelligence_result.risk_level,

            status="COMPLETED",

        )


        self.deal_repository.save_deal(

            deal_record

        )


        print()

        print(
            "Deal Saved:"
        )

        print(deal_record)



        print()

        print(
            "STEP 7 - Learning System Update"
        )



        learning_record = LearningRecord(

            deal_id=context.deal_id,

            lesson=(

                "High scoring acquisition opportunity detected "
                "with strong profit margin."

            ),

            category="SUCCESSFUL_ACQUISITION",

            created_at=datetime.now(timezone.utc),

        )



        self.learning_repository.save(

            learning_record

        )


        patterns = self.pattern_detector.analyze(

            self.learning_repository.get_all()

        )


        print()

        print(
            "Learning Record:"
        )

        print(
            learning_record
        )


        print()

        print(
            "Detected Patterns:"
        )

        print(
            patterns
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


            "stored_deal":
                deal_record,


            "learning_record":
                learning_record,


            "patterns":
                patterns,


            "recommendation":
                intelligence_result.recommendation,


            "status":
                "COMPLETED",

        }