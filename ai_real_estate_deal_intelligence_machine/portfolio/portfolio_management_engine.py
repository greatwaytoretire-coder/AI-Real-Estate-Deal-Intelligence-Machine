from dataclasses import dataclass, field
from enum import Enum


class PortfolioStatus(str, Enum):

    ACTIVE = "Active"
    REVIEW = "Review"
    OPTIMIZATION = "Optimization"



@dataclass
class PortfolioRecord:

    portfolio_id: str
    owner_id: str

    assets: list[str] = field(default_factory=list)

    total_value: float = 0
    total_equity: float = 0

    monthly_income: float = 0
    monthly_expenses: float = 0

    status: PortfolioStatus = PortfolioStatus.ACTIVE

    notes: list[str] = field(default_factory=list)



class PortfolioManagementEngine:


    def __init__(self):

        self.portfolios = {}



    def create_portfolio(
        self,
        portfolio_id: str,
        owner_id: str,
    ):

        portfolio = PortfolioRecord(
            portfolio_id=portfolio_id,
            owner_id=owner_id,
        )

        portfolio.notes.append(
            "Portfolio created."
        )

        self.portfolios[portfolio_id] = portfolio

        return portfolio



    def get_portfolios(self):

        return list(
            self.portfolios.values()
        )



    def add_asset(
        self,
        portfolio_id: str,
        asset_id: str,
    ):

        portfolio = self._get_portfolio(
            portfolio_id
        )

        portfolio.assets.append(
            asset_id
        )

        portfolio.notes.append(
            f"Asset added: {asset_id}"
        )

        return portfolio



    def update_financials(
        self,
        portfolio_id: str,
        total_value: float,
        total_equity: float,
        monthly_income: float,
        monthly_expenses: float,
    ):

        portfolio = self._get_portfolio(
            portfolio_id
        )

        portfolio.total_value = total_value
        portfolio.total_equity = total_equity
        portfolio.monthly_income = monthly_income
        portfolio.monthly_expenses = monthly_expenses

        return portfolio



    def calculate_performance(
        self,
        portfolio_id: str,
    ):

        portfolio = self._get_portfolio(
            portfolio_id
        )

        return {
            "portfolio_id": portfolio.portfolio_id,
            "cash_flow":
                portfolio.monthly_income
                -
                portfolio.monthly_expenses,
            "equity": portfolio.total_equity,
            "value": portfolio.total_value,
        }



    def update_status(
        self,
        portfolio_id: str,
        new_status: PortfolioStatus,
        note: str,
    ):

        portfolio = self._get_portfolio(
            portfolio_id
        )

        portfolio.status = new_status

        portfolio.notes.append(
            note
        )

        return portfolio



    def _get_portfolio(
        self,
        portfolio_id: str,
    ):

        if portfolio_id not in self.portfolios:

            raise ValueError(
                "Portfolio not found."
            )

        return self.portfolios[portfolio_id]