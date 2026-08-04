from dataclasses import dataclass


@dataclass
class PropertyManagementReport:

    report_id: str
    property_id: str
    income: float
    expenses: float
    noi: float
    period: str


class PropertyManagementReportsEngine:

    def __init__(self):

        self.reports = []


    def create_report(
        self,
        report_id: str,
        property_id: str,
        income: float,
        expenses: float,
        period: str,
    ):

        if income < 0:
            raise ValueError(
                "Income cannot be negative."
            )

        if expenses < 0:
            raise ValueError(
                "Expenses cannot be negative."
            )


        noi = income - expenses


        report = {
            "report_id": report_id,
            "property_id": property_id,
            "income": income,
            "expenses": expenses,
            "noi": noi,
            "period": period,
        }


        self.reports.append(report)


        return report


    def get_reports(self):

        return self.reports