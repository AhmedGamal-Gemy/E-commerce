from configs.settings import get_settings
from typing import Optional
from api.schemas.PaymobResponseSchema import BillingData, Item, IntentionDetail, PaymentKey, PaymentMethod, CreationExtras, Extras
import asyncio
from api.schemas.PaymobResponseSchema import PaymentIntentionResponse
from datetime import datetime, timezone
from typing import List
from api.schemas.RequestSchemas import OrderItemRequest
import httpx
from core.logging import get_logger

logger = get_logger(__name__)
settings = get_settings()

class PaymobClient:
    BASE_URL = "https://accept.paymob.com/v1/intention/"
    PUBLIC_KEY = settings.PAYMOB_PUBLIC_KEY
    SECRET_KEY = settings.PAYMOB_SECRET_KEY
    INTEGRATION_ID = settings.PAYMOB_INTEGRATION_ID

    async def create_intention(
        self, 
        amount: float, 
        order_id: str,
        order_items: List[OrderItemRequest], 
        email: str,
        address : str,
        first_name: str,
        last_name: str,
        phone_number: str

    )-> PaymentIntentionResponse:

        logger.debug(f"first name is {first_name}, last name is {last_name}, order items is {order_items}")
        body = {
        "amount": float(amount * 100),  # Cents
        "currency": "EGP",
        "payment_methods": [int(self.INTEGRATION_ID)],
        "items": [
            {
                "name": item.product_id[:50],
                "amount": float(item.product_price * 100), 
                "description": f"Quantity: {item.quantity}",  
                "quantity": item.quantity
            } for item in order_items
        ],
        "billing_data": {
            "apartment": "dumy",
            "first_name": first_name,
            "last_name": last_name,
            "street": address,
            "building": "dumy",
            "phone_number": phone_number,
            "city": "dumy",
            "country": "dumy",
            "email": email,
            "floor": "dumy",
            "state": "dumy"
        },
        "extras": {"ee": 22},
        "special_reference": order_id or "no_id",
        "notification_url": "https://www.google.com/",  
        "redirection_url": "https://www.google.com/"   
        }
        logger.debug(body)

        headers = {
                    "Authorization": f"Bearer {self.SECRET_KEY}",
                    "Content-Type": "application/json"
                }

        async with httpx.AsyncClient() as client:
                response = await client.post(self.BASE_URL, json=body, headers=headers)
                response.raise_for_status()  # Raises for 4xx/5xx; accepts 200, 201, etc.
                return PaymentIntentionResponse(**response.json())

    async def create_fake_intention(
        self, 
        amount: float, 
        order_id: Optional[str], 
        email: str
    )-> PaymentIntentionResponse:
        
        # Optional: Simulate API delay
        await asyncio.sleep(1)  # 1-second delay to mimic network call
        
        # Fake amount in smallest unit (e.g., cents/piastres)
        fake_amount_cents = int(amount * 100)
        
        # Fake billing data (minimal, as per schema)
        fake_billing = BillingData(
            apartment="NA",
            floor="NA",
            first_name="Test",
            last_name="User",
            street="NA",
            building="NA",
            phone_number="+1234567890",
            shipping_method="PKG",
            city="Cairo",
            country="EG",
            state="NA",
            email=email,
            postal_code="12345"
        )
        
        # Fake items (at least one, as per typical API requirements)
        fake_items = [
            Item(
                name="Test Product",
                amount=fake_amount_cents,
                description="Mock item for testing",
                quantity=1,
                image="https://example.com/image.jpg"
            )
        ]
        
        # Fake intention detail
        fake_detail = IntentionDetail(
            amount=fake_amount_cents,
            items=fake_items,
            currency="EGP",
            billing_data=fake_billing
        )
        
        # Fake payment keys (one example)
        fake_payment_keys = [
            PaymentKey(
                integration=self.INTEGRATION_ID,  # Use the class var
                key="fake_payment_key",
                gateway_type="card",
                iframe_id="fake_iframe_123",
                order_id=123456,  # Fake int order ID
                redirection_url="https://example.com/redirect",
                save_card=False
            )
        ]
        
        # Fake payment methods (one example)
        fake_payment_methods = [
            PaymentMethod(
                integration_id=self.INTEGRATION_ID,
                alias="Visa",
                name="Card",
                method_type="card",
                currency="EGP",
                live=False,  # Test mode
                use_cvc_with_moto=True
            )
        ]
        
        # Fake extras
        fake_creation_extras = CreationExtras(
            ee=1,
            merchant_order_id=order_id or "fake_order_123"
        )
        fake_extras = Extras(
            creation_extras=fake_creation_extras
        )
        
        # Construct and return fake response
        return PaymentIntentionResponse(
            payment_keys=fake_payment_keys,
            redirection_url="https://example.com/fake_redirect",
            intention_order_id=123456,
            id="fake_intention_abc123",
            intention_detail=fake_detail,
            client_secret="fake_client_secret_1234567890",  # Key for checkout URL
            payment_methods=fake_payment_methods,
            special_reference="fake_ref_xyz",
            extras=fake_extras,
            confirmed=False,
            status="intended",
            created=datetime.now(timezone.utc),
            card_detail=None,
            card_tokens=[],
            object="payment_intention"
        )