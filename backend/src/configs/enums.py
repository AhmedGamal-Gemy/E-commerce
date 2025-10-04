from enum import Enum

class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

class ReportType(Enum):
    SALES = "sales"
    INVENTORY = "inventory"
    CUSTOMER = "customer"