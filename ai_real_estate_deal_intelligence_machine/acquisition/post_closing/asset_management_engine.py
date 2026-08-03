from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List


class AssetStatus(Enum):
    ACQUIRED = "Acquired"
    ACTIVE = "Active"
    RENOVATION = "Renovation"
    RENTED = "Rented"
    LISTED_FOR_SALE = "Listed For Sale"
    SOLD = "Sold"


@dataclass
class AssetRecord:
    asset_id: str
    property_address: str
    acquisition_price: float
    closing_date: str
    strategy: str

    status: AssetStatus = AssetStatus.ACQUIRED

    monthly_income: float = 0.0
    monthly_expenses: float = 0.0

    notes: List[str] = field(default_factory=list)


class AssetManagementEngine:

    def __init__(self):
        self.assets: Dict[str, AssetRecord] = {}

    def create_asset(
        self,
        asset_id: str,
        property_address: str,
        acquisition_price: float,
        closing_date: str,
        strategy: str,
    ) -> AssetRecord:

        asset = AssetRecord(
            asset_id=asset_id,
            property_address=property_address,
            acquisition_price=acquisition_price,
            closing_date=closing_date,
            strategy=strategy,
            notes=[
                "Asset created after closing."
            ],
        )

        self.assets[asset_id] = asset

        return asset


    def get_assets(self) -> List[AssetRecord]:

        return list(self.assets.values())


    def update_status(
        self,
        asset_id: str,
        new_status: AssetStatus,
        note: str,
    ) -> AssetRecord:

        asset = self.assets.get(asset_id)

        if not asset:
            raise ValueError("Asset not found.")

        asset.status = new_status
        asset.notes.append(note)

        return asset


    def add_income(
        self,
        asset_id: str,
        amount: float,
    ) -> AssetRecord:

        asset = self.assets.get(asset_id)

        if not asset:
            raise ValueError("Asset not found.")

        asset.monthly_income += amount

        return asset


    def add_expense(
        self,
        asset_id: str,
        amount: float,
    ) -> AssetRecord:

        asset = self.assets.get(asset_id)

        if not asset:
            raise ValueError("Asset not found.")

        asset.monthly_expenses += amount

        return asset


    def calculate_performance(
        self,
        asset_id: str,
    ) -> dict:

        asset = self.assets.get(asset_id)

        if not asset:
            raise ValueError("Asset not found.")

        cash_flow = (
            asset.monthly_income -
            asset.monthly_expenses
        )

        return {
            "asset_id": asset.asset_id,
            "monthly_income": asset.monthly_income,
            "monthly_expenses": asset.monthly_expenses,
            "monthly_cash_flow": cash_flow,
        }