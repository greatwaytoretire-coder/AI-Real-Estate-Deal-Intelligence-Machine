from ai_real_estate_deal_intelligence_machine.auth.hashing import (
    hash_password,
    verify_password,
)


def test_password_hashing():
    password = "SecurePassword123!"

    hashed = hash_password(password)

    assert hashed != password

    assert verify_password(
        password,
        hashed,
    )

    assert not verify_password(
        "WrongPassword",
        hashed,
    )