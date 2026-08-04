from dataclasses import dataclass


@dataclass
class PropertyFinancialRecord:

    record_id: str
    property_id: str
    income: float
    expenses: float
    period: str

    @property
    def noi(self):
        return self.income - self.expenses


class PropertyFinancialsEngine:

    def __init__(self):

        self.records = []


    def create_financial_record(
        self,
        record_id: str,
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


        record = PropertyFinancialRecord(
            record_id=record_id,
            property_id=property_id,
            income=income,
            expenses=expenses,
            period=period,
        )


        self.records.append(record)

        return {
            "record_id": record.record_id,
            "property_id": record.property_id,
            "income": record.income,
            "expenses": record.expenses,
            "noi": record.noi,
            "period": record.period,
        }


    def get_financial_records(self):

        return [
            {
                "record_id": record.record_id,
                "property_id": record.property_id,
                "income": record.income,
                "expenses": record.expenses,
                "noi": record.noi,
                "period": record.period,
            }
            for record in self.records
        ]