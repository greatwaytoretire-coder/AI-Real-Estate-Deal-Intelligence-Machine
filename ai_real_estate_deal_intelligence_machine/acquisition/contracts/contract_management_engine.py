from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List


class ContractStatus(str, Enum):
    DRAFT = "Draft"
    SENT = "Sent"
    SIGNED = "Signed"
    DUE_DILIGENCE = "Due Diligence"
    INSPECTION = "Inspection"
    TITLE_REVIEW = "Title Review"
    CLOSING_SCHEDULED = "Closing Scheduled"
    CLOSED = "Closed"


@dataclass
class ContractRecord:
    contract_id: str
    seller_id: str
    property_address: str
    purchase_price: float
    earnest_money: float
    status: ContractStatus
    notes: List[str] = field(default_factory=list)


class ContractManagementEngine:
    """
    Manages contracts from creation through closing.

    Workflow

    Negotiation Accepted
            |
            v
    Contract Created
            |
            v
    Due Diligence
            |
            v
    Inspection
            |
            v
    Title Review
            |
            v
    Closing Scheduled
            |
            v
    Closed
    """

    def __init__(self) -> None:
        self.contracts: List[ContractRecord] = [
            ContractRecord(
                contract_id="CONTRACT-001",
                seller_id="SELLER-001",
                property_address="123 Main Street",
                purchase_price=150000.00,
                earnest_money=5000.00,
                status=ContractStatus.DRAFT,
                notes=[
                    "Contract initialized."
                ],
            )
        ]

    def get_contracts(self) -> List[ContractRecord]:
        return self.contracts

    def get_contract(self, contract_id: str) -> ContractRecord:
        for contract in self.contracts:
            if contract.contract_id == contract_id:
                return contract

        raise ValueError("Contract not found.")

    def update_status(
        self,
        contract_id: str,
        new_status: ContractStatus,
        note: str,
    ) -> ContractRecord:

        contract = self.get_contract(contract_id)

        contract.status = new_status
        contract.notes.append(note)

        return contract

    def create_contract(
        self,
        contract_id: str,
        seller_id: str,
        property_address: str,
        purchase_price: float,
        earnest_money: float,
    ) -> ContractRecord:

        contract = ContractRecord(
            contract_id=contract_id,
            seller_id=seller_id,
            property_address=property_address,
            purchase_price=purchase_price,
            earnest_money=earnest_money,
            status=ContractStatus.DRAFT,
            notes=[
                "Contract created."
            ],
        )

        self.contracts.append(contract)

        return contract