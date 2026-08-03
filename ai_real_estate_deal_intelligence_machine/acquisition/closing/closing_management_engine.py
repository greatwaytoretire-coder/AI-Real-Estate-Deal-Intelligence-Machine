from dataclasses import dataclass, field
from enum import Enum



class ClosingStatus(str, Enum):

    SCHEDULED = "Scheduled"
    TITLE_REVIEW = "Title Review"
    FUNDED = "Funded"
    COMPLETED = "Completed"



@dataclass
class ClosingRecord:

    closing_id: str
    contract_id: str
    property_address: str
    title_company: str
    closing_date: str
    status: ClosingStatus = ClosingStatus.SCHEDULED
    documents: list[str] = field(default_factory=list)
    notes: list[str] = field(
        default_factory=lambda: [
            "Closing created."
        ]
    )



class ClosingManagementEngine:


    def __init__(self):

        self._closings = {}



    def create_closing(
        self,
        closing_id: str,
        contract_id: str,
        property_address: str,
        title_company: str,
        closing_date: str,
    ):

        closing = ClosingRecord(
            closing_id=closing_id,
            contract_id=contract_id,
            property_address=property_address,
            title_company=title_company,
            closing_date=closing_date,
        )


        self._closings[closing_id] = closing

        return closing



    def get_closings(self):

        return list(
            self._closings.values()
        )



    def update_status(
        self,
        closing_id: str,
        new_status: ClosingStatus,
        note: str,
    ):


        if closing_id not in self._closings:

            raise ValueError(
                "Closing not found."
            )


        closing = self._closings[closing_id]

        closing.status = new_status

        closing.notes.append(note)


        return closing



    def add_document(
        self,
        closing_id: str,
        document_name: str,
    ):


        if closing_id not in self._closings:

            raise ValueError(
                "Closing not found."
            )


        closing = self._closings[closing_id]

        closing.documents.append(
            document_name
        )


        return closing