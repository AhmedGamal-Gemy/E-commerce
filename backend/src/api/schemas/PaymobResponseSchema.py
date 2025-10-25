from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime


class BillingData(BaseModel):
    apartment: str
    floor: str
    first_name: str
    last_name: str
    street: str
    building: str
    phone_number: str
    shipping_method: str
    city: str
    country: str
    state: str
    email: str
    postal_code: str


class Item(BaseModel):
    name: str
    amount: int
    description: str
    quantity: int
    image: Optional[str] = None


class IntentionDetail(BaseModel):
    amount: int
    items: List[Item]
    currency: str
    billing_data: BillingData


class PaymentKey(BaseModel):
    integration: int
    key: str
    gateway_type: str
    iframe_id: Optional[str] = None
    order_id: int
    redirection_url: str
    save_card: bool


class PaymentMethod(BaseModel):
    integration_id: int
    alias: Optional[str] = None
    name: Optional[str] = None
    method_type: str
    currency: str
    live: bool
    use_cvc_with_moto: bool


class CreationExtras(BaseModel):
    ee: int
    merchant_order_id: str


class Extras(BaseModel):
    creation_extras: CreationExtras
    confirmation_extras: Optional[Dict[str, Any]] = None


class PaymentIntentionResponse(BaseModel):
    payment_keys: List[PaymentKey]
    redirection_url: str
    intention_order_id: int
    id: str
    intention_detail: IntentionDetail
    client_secret: str
    payment_methods: List[PaymentMethod]
    special_reference: str
    extras: Extras
    confirmed: bool
    status: str
    created: datetime  # parsed into datetime automatically
    card_detail: Optional[Dict[str, Any]] = None
    card_tokens: List[Any]
    object: str
