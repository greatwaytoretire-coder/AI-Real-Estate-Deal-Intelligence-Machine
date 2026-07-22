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
        self.db_client = DatabaseClient(database_path=self.db_path)
        self.auth_service = AuthenticationService(db_client=self.db_client)

    def tearDown(self):
        self.db_path.unlink(missing_ok=True)

    def test_user_registration_and_login(self):
        """
        PHASE 39: Verify user registration and login functionality.
        """
        email = "test@example.com"
        password = "secure_password_123"
        org_id = "org-test"

        # 1. Successful registration
        user = self.auth_service.register_user(email, password, org_id)
        self.assertIsNotNone(user)
        self.assertEqual(user.email, email)

        # 2. Prevent duplicate registration
        duplicate_user = self.auth_service.register_user(email, password, org_id)
        self.assertIsNone(duplicate_user)

        # 3. Successful login
        logged_in_user = self.auth_service.login_user(email, password)
        self.assertIsNotNone(logged_in_user)
        self.assertEqual(logged_in_user.user_id, user.user_id)

    def test_failed_login_attempts(self):
        """
        PHASE 39: Verify that incorrect login attempts fail.
        """
        email = "test2@example.com"
        password = "correct_password"
        self.auth_service.register_user(email, password, "org-test")

        # Incorrect password
        self.assertIsNone(self.auth_service.login_user(email, "wrong_password"))

        # Non-existent user
        self.assertIsNone(self.auth_service.login_user("nouser@example.com", "any_password"))

    def test_authorization_and_permissions(self):
        """
        PHASE 39: Verify role-based access control and organization isolation.
        """
        authz_service = AuthorizationService()

        # Create users with different roles
        admin_user = User(organization_id="org-A", role=Role.ADMIN)
        viewer_user = User(organization_id="org-A", role=Role.VIEWER)
        other_org_admin = User(organization_id="org-B", role=Role.ADMIN)

        # 1. Test role access
        self.assertTrue(authz_service.can(admin_user, Permission.MANAGE_USERS))
        self.assertTrue(authz_service.can(viewer_user, Permission.VIEW_DEALS))

        # 2. Test unauthorized access
        self.assertFalse(authz_service.can(viewer_user, Permission.MANAGE_USERS))

        # 3. Test organization isolation
        # Create a mock resource belonging to org-A
        class MockResource:
            def __init__(self, org_id):
                self.organization_id = org_id

        resource_A = MockResource(org_id="org-A")

        # Admin from org-A can access resource from org-A
        self.assertTrue(authz_service.can(admin_user, Permission.MANAGE_DEALS, resource_A))

        # Admin from org-B CANNOT access resource from org-A
        self.assertFalse(authz_service.can(other_org_admin, Permission.MANAGE_DEALS, resource_A))