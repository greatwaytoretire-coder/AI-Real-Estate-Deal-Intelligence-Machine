from dataclasses import dataclass
from enum import Enum


class InvestmentRecommendation(str, Enum):

    HOLD = "Hold"
    SELL = "Sell"
    OPTIMIZE = "Optimize"
    REVIEW = "Review"



@dataclass
class PortfolioAnalysis:

    portfolio_id: str

    health_score: int

    roi: float

    cash_on_cash_return: float

    cap_rate: float

    risk_score: int

    recommendation: InvestmentRecommendation

    reasons: list[str]



class PortfolioOptimizer:


    def analyze_portfolio(
        self,
        portfolio_id: str,
        total_value: float,
        equity: float,
        annual_income: float,
        annual_expenses: float,
    ):


        if total_value <= 0:

            raise ValueError(
                "Portfolio value must be greater than zero."
            )


        net_income = (
            annual_income
            -
            annual_expenses
        )


        roi = (
            net_income / total_value
        ) * 100


        cash_on_cash = (
            net_income / equity
        ) * 100 if equity else 0


        cap_rate = roi


        health_score = 100


        reasons = []


        if net_income <= 0:

            health_score -= 40

            reasons.append(
                "Negative cash flow detected."
            )


        if annual_expenses > annual_income * 0.40:

            health_score -= 20

            reasons.append(
                "High expense ratio."
            )


        if equity < total_value * 0.20:

            health_score -= 15

            reasons.append(
                "Low equity position."
            )


        if health_score >= 80:

            recommendation = (
                InvestmentRecommendation.HOLD
            )


        elif health_score >= 60:

            recommendation = (
                InvestmentRecommendation.OPTIMIZE
            )


        else:

            recommendation = (
                InvestmentRecommendation.REVIEW
            )


        return PortfolioAnalysis(

            portfolio_id=portfolio_id,

            health_score=max(
                health_score,
                0
            ),

            roi=round(
                roi,
                2
            ),

            cash_on_cash_return=round(
                cash_on_cash,
                2
            ),

            cap_rate=round(
                cap_rate,
                2
            ),

            risk_score=100 - max(
                health_score,
                0
            ),

            recommendation=recommendation,

            reasons=reasons,
        )