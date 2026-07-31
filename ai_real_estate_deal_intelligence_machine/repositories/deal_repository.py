class DealRepository:

    def __init__(self):
        pass


    def get_deal(self, deal_id: str):

        return {
            "property_id": deal_id,
            "address": "123 Example Street",
            "status": "discovered"
        }


    def save_deal(self, deal):

        return {
            "saved": True,
            "deal": deal
        }