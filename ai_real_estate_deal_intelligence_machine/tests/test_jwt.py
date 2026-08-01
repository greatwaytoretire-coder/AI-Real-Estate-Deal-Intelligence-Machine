from ai_real_estate_deal_intelligence_machine.auth.jwt import (
    create_access_token,
    decode_access_token,
)


def test_create_and_decode_jwt():

    payload = {
        "sub": "user123",
        "role": "investor",
    }

    token = create_access_token(payload)

    decoded = decode_access_token(token)

    assert decoded["sub"] == "user123"
    assert decoded["role"] == "investor"