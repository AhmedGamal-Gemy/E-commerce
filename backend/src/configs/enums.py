from enum import Enum

class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

class ReportType(Enum):
    SALES = "sales"
    INVENTORY = "inventory"
    CUSTOMER = "customer"

class CollectionNames(Enum):
    USERS = "users"
    PRODUCTS = "products"
    REPORTS = "reports"
    CATEGORIES = "categories"
    ORDERS = "orders"