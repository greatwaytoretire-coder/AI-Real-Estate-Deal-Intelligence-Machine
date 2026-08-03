from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List


class DueDiligenceStatus(str, Enum):
    INITIATED = "Initiated"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    FAILED = "Failed"



@dataclass
class DueDiligenceReview:

    review_id: str
    property_address: str
    contract_id: str
    status: DueDiligenceStatus = DueDiligenceStatus.INITIATED
    notes: List[str] = field(default_factory=list)



class DueDiligenceEngine:


    def __init__(self):

        self._reviews: Dict[str, DueDiligenceReview] = {}



    def create_review(
        self,
        review_id: str,
        property_address: str,
        contract_id: str,
    ) -> DueDiligenceReview:


        review = DueDiligenceReview(
            review_id=review_id,
            property_address=property_address,
            contract_id=contract_id,
        )


        review.notes.append(
            "Due diligence review created."
        )


        self._reviews[review_id] = review


        return review



    def get_reviews(self) -> List[DueDiligenceReview]:

        return list(self._reviews.values())



    def get_review(
        self,
        review_id: str,
    ) -> DueDiligenceReview:


        review = self._reviews.get(review_id)


        if review is None:

            raise ValueError(
                "Due diligence review not found."
            )


        return review



    def update_status(
        self,
        review_id: str,
        new_status: DueDiligenceStatus,
        note: str,
    ) -> DueDiligenceReview:


        review = self.get_review(
            review_id
        )


        review.status = new_status


        review.notes.append(
            note
        )


        return review