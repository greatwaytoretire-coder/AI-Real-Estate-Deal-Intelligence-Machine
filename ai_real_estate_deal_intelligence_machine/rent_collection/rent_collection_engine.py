from typing import List, Dict


class RentCollectionEngine:


    def __init__(self):

        self.payments: List[Dict] = []



    def create_rent_payment(
        self,
        payment_id: str,
        tenant_id: str,
        property_id: str,
        amount: float,
        payment_date: str,
    ):

        if amount <= 0:

            raise ValueError(
                "Payment amount must be greater than zero."
            )


        payment = {

            "payment_id": payment_id,
            "tenant_id": tenant_id,
            "property_id": property_id,
            "amount": amount,
            "payment_date": payment_date,

        }


        self.payments.append(payment)


        return payment



    # Backward compatibility
    def create_payment(
        self,
        payment_id: str,
        tenant_id: str,
        property_id: str,
        amount: float,
        payment_date: str,
    ):

        return self.create_rent_payment(
            payment_id=payment_id,
            tenant_id=tenant_id,
            property_id=property_id,
            amount=amount,
            payment_date=payment_date,
        )



    def get_rent_payments(self):

        return self.payments



    # Backward compatibility
    def get_payments(self):

        return self.get_rent_payments()