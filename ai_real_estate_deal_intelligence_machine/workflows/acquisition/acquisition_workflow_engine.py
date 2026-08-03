from dataclasses import dataclass
from enum import Enum


class AcquisitionStage(Enum):

    NEW_LEAD = "New Lead"

    CONTACT_ATTEMPTED = "Contact Attempted"

    CONVERSATION_STARTED = "Conversation Started"

    OFFER_GENERATED = "Offer Generated"

    OFFER_SENT = "Offer Sent"

    NEGOTIATION = "Negotiation"

    CONTRACT_SIGNED = "Contract Signed"

    CLOSED = "Closed"



@dataclass
class AcquisitionWorkflow:

    seller_id: str

    property_address: str

    current_stage: AcquisitionStage

    offer_amount: float

    notes: list[str]



class AcquisitionWorkflowEngine:
    """
    Manages seller acquisition workflow progression.

    Flow:

    Seller Lead
          |
          v
    Acquisition Pipeline
          |
          v
    Workflow Stage Tracking
          |
          v
    Closed Transaction
    """


    def __init__(self):

        self.workflows = [

            AcquisitionWorkflow(
                seller_id="SELLER-001",
                property_address="123 Main Street",
                current_stage=AcquisitionStage.NEW_LEAD,
                offer_amount=0,
                notes=[
                    "High motivation seller detected."
                ],
            ),

        ]


    def advance_stage(
        self,
        seller_id: str,
        new_stage: AcquisitionStage,
        note: str,
    ) -> AcquisitionWorkflow:


        for workflow in self.workflows:

            if workflow.seller_id == seller_id:

                workflow.current_stage = new_stage

                workflow.notes.append(note)

                return workflow


        raise ValueError(
            "Seller workflow not found."
        )



    def get_workflows(
        self,
    ) -> list[AcquisitionWorkflow]:

        return self.workflows