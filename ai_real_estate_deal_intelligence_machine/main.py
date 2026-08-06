from ai_real_estate_deal_intelligence_machine.runtime.pipeline import (
    AutonomousPipeline,
)

from ai_real_estate_deal_intelligence_machine.application_service import (
    ApplicationService,
)

from ai_real_estate_deal_intelligence_machine.command_center.autonomous_command_center import (
    AutonomousCommandCenter,
)

from ai_real_estate_deal_intelligence_machine.dashboard.deal_dashboard import (
    DealDashboard,
)


def build_application():

    pipeline = AutonomousPipeline()

    command_center = AutonomousCommandCenter()

    dashboard = DealDashboard()


    application = ApplicationService(

        pipeline=pipeline,

        command_center=command_center,

        dashboard=dashboard,

    )


    return application



def main():

    print("=" * 70)

    print(
        "AI REAL ESTATE DEAL INTELLIGENCE MACHINE"
    )

    print(
        "AUTONOMOUS INVESTMENT SYSTEM ONLINE"
    )

    print("=" * 70)


    application = build_application()


    result = application.analyze_deal(
        deal_id="DEAL-001"
    )


    print()

    print("=" * 70)

    print(
        "FINAL INVESTMENT RECOMMENDATION"
    )

    print("=" * 70)


    print()

    print(
        result
    )



if __name__ == "__main__":

    main()