import unittest
from pathlib import Path

from ai_real_estate_deal_intelligence_machine.db_client import DatabaseClient
from ai_real_estate_deal_intelligence_machine.phase39 import (
    AuthenticationService,
    AuthorizationService,
    Permission,
    Role,
    User,
)


class Phase39AuthenticationTest(unittest.TestCase):

    def setUp(self):
        self.db_path = Path("data/test_phase39.db")
        self.db_path.unlink(missing_ok=True)

        self.db = DatabaseClient(self.db_path)
        self.auth = AuthenticationService(self.db)

    def tearDown(self):
        self.db.close()
        self.db_path.unlink(missing_ok=True)

    def test_user_registration_and_login(self):
        email = "test@example.com"
        password = "secure_password_123"
        org_id = "org-test"

        user = self.auth.register_user(email, password, org_id)
        self.assertIsNotNone(user)
        self.assertEqual(user.email, email)

        duplicate_user = self.auth.register_user(email, password, org_id)
        self.assertIsNone(duplicate_user)

        logged_in_user = self.auth.login_user(email, password)
        self.assertIsNotNone(logged_in_user)
        self.assertEqual(logged_in_user.user_id, user.user_id)

    def test_failed_login_attempts(self):
        email = "test2@example.com"
        password = "correct_password"

        self.auth.register_user(email, password, "org-test")

        self.assertIsNone(
            self.auth.login_user(email, "wrong_password")
        )

        self.assertIsNone(
            self.auth.login_user("nouser@example.com", "any_password")
        )

    def test_authorization_and_permissions(self):
        authz_service = AuthorizationService()

        admin_user = User(
            organization_id="org-A",
            role=Role.ADMIN.value,
        )

        viewer_user = User(
            organization_id="org-A",
            role=Role.VIEWER.value,
        )

        other_org_admin = User(
            organization_id="org-B",
            role=Role.ADMIN.value,
        )

        self.assertTrue(
            authz_service.can(
                admin_user,
                Permission.MANAGE_USERS,
            )
        )

        self.assertTrue(
            authz_service.can(
                viewer_user,
                Permission.VIEW_DEALS,
            )
        )

        self.assertFalse(
            authz_service.can(
                viewer_user,
                Permission.MANAGE_USERS,
            )
        )

        class MockResource:
            def __init__(self, org_id):
                self.organization_id = org_id

        resource_A = MockResource(org_id="org-A")

        self.assertTrue(
            authz_service.can(
                admin_user,
                Permission.MANAGE_DEALS,
                resource_A,
            )
        )

        self.assertFalse(
            authz_service.can(
                other_org_admin,
                Permission.MANAGE_DEALS,
                resource_A,
            )
        )