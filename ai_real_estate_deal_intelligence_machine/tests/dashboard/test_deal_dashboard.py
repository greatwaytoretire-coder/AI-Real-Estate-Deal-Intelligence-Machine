from ai_real_estate_deal_intelligence_machine.dashboard.deal_dashboard import (
    DealDashboard,
)


def test_dashboard_tracks_deal_activity():

    dashboard = DealDashboard()

    dashboard.register_deal(
        "DEAL001",
        "123 Main Street",
        "underwriting",
    )

    dashboard.register_agent(
        "UnderwritingAgent",
        "Analyzing comps",
    )

    dashboard.add_recommendation(
        "DEAL001",
        "Proceed with seller negotiation",
        0.91,
    )

    snapshot = dashboard.snapshot()

    assert len(snapshot.deals) == 1
    assert len(snapshot.agents) == 1
    assert len(snapshot.recommendations) == 1
    assert snapshot.recommendations[0].confidence_score == 0.91