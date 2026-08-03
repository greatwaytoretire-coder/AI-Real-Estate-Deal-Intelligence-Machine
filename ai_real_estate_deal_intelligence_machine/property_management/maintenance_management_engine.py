from dataclasses import dataclass
from enum import Enum


class WorkOrderStatus(str, Enum):
    OPEN = "OPEN"
    ASSIGNED = "ASSIGNED"
    COMPLETED = "COMPLETED"


class PriorityLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    EMERGENCY = "EMERGENCY"


@dataclass
class WorkOrder:

    work_order_id: str
    property_id: str
    description: str
    priority: PriorityLevel
    estimated_cost: float
    vendor: str | None = None
    status: WorkOrderStatus = WorkOrderStatus.OPEN


class MaintenanceManagementEngine:

    def __init__(self):

        self.work_orders = {}


    def create_work_order(
        self,
        work_order_id: str,
        property_id: str,
        description: str,
        priority: PriorityLevel,
        estimated_cost: float,
    ):

        order = WorkOrder(
            work_order_id=work_order_id,
            property_id=property_id,
            description=description,
            priority=priority,
            estimated_cost=estimated_cost,
        )

        self.work_orders[work_order_id] = order

        return order


    def assign_vendor(
        self,
        work_order_id: str,
        vendor: str,
    ):

        order = self.get_work_order(work_order_id)

        order.vendor = vendor
        order.status = WorkOrderStatus.ASSIGNED

        return order


    def complete_work_order(
        self,
        work_order_id: str,
    ):

        order = self.get_work_order(work_order_id)

        order.status = WorkOrderStatus.COMPLETED

        return order


    def get_work_order(
        self,
        work_order_id: str,
    ):

        order = self.work_orders.get(work_order_id)

        if order is None:
            raise ValueError(
                "Work order not found."
            )

        return order


    def get_work_orders(self):

        return list(self.work_orders.values())