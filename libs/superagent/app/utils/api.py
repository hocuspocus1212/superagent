import logging
import uuid

import jwt
from decouple import config
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.utils.prisma import prisma

logger = logging.getLogger(__name__)
security = HTTPBearer()


def handle_exception(e):
    print("apps>utils>api.py>handle_exception","line 16")
    logger.exception(e)
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
    )


def generate_jwt(data: dict):
    print("apps>utils>api.py>generate_jwt","line 24")
    # for randomness
    data.update({"jti": str(uuid.uuid4())})

    token = jwt.encode({**data}, config("JWT_SECRET"), algorithm="HS256")
    return token


def decode_jwt(token: str):
    print("apps>utils>api.py>decode_jwt","line 33")
    return jwt.decode(token, config("JWT_SECRET"), algorithms=["HS256"])


async def get_current_api_user(
    authorization: HTTPAuthorizationCredentials = Security(security),
):
    print("apps>utils>api.py>get_current_api_user","line 40")
    token = authorization.credentials
    decoded_token = decode_jwt(token)
    api_user = await prisma.apiuser.find_unique(
        where={"id": decoded_token.get("api_user_id")}
    )
    if config("STRIPE_SECRET_KEY", None):
        import stripe

        stripe.api_key = config("STRIPE_SECRET_KEY")

        data = stripe.Customer.list(
            email=api_user.email, expand=["data.subscriptions"]
        ).data
        has_subscription = False
        if len(data) > 0:
            customer = data[0]
            subscription = customer.subscriptions.data[0]["items"]["data"]
            has_subscription = any(sub["plan"]["active"] for sub in subscription)

        if not has_subscription:
            logger.error(f"User {api_user.id} has no active subscription")
            raise HTTPException(
                status_code=402, detail="You have no active subscription"
            )

    if not api_user:
        raise HTTPException(status_code=401, detail="Invalid token or expired token")
    return api_user
