from dataclasses import dataclass
from typing import List


@dataclass
class Inspection:

    inspection_id: str
    property_id: str
    inspector_name: str
    inspection_date: str
    condition: str
    status: str = "COMPLETED"



class InspectionManagementEngine:

    def __init__(self):

        self.inspections: List[Inspection] = []


    def create_inspection(
        self,
        inspection_id: str,
        property_id: str,
        inspector_name: str,
        inspection_date: str,
        condition: str,
    ):

        if not inspector_name:

            raise ValueError(
                "Inspector name is required."
            )


        inspection = Inspection(
            inspection_id=inspection_id,
            property_id=property_id,
            inspector_name=inspector_name,
            inspection_date=inspection_date,
            condition=condition,
        )


        self.inspections.append(
            inspection
        )

        return inspection



    def get_inspection(
        self,
        inspection_id: str
    ):

        for inspection in self.inspections:

            if inspection.inspection_id == inspection_id:

                return inspection


        raise ValueError(
            "Inspection not found."
        )



    def get_inspections(self):

        return self.inspections



    def update_status(
        self,
        inspection_id: str,
        status: str
    ):

        inspection = self.get_inspection(
            inspection_id
        )

        inspection.status = status

        return inspection