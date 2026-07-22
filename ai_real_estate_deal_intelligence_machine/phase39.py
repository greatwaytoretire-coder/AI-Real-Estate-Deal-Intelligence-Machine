from __future__ import annotations

import hashlib
import secrets
from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4
from typing import Any, Dict, Optional, Set

from .db_client import DatabaseClient
from .phase25 import PendingActionDashboard
from .phase29 import MarketConfig, ScalingManager
from .phase30 import CanonicalProperty
from .phase32 import LivePilotRunner
from .phase33 import ValidationManager


@dataclass
class Organization:
    """Represents a tenant organization in the SaaS system."""

    organization_id: str = field(default_factory=lambda: f"org_{uuid4()}")
    name: str = ""


class Role(str, Enum):
    """Defines the user roles within an organization."""

    OWNER = "owner"
    ADMIN = "admin"
    INVESTOR = "investor"
    ACQUISITIONS = "acquisitions_manager"
    DISPOSITIONS = "dispositions_manager"
    ANALYST = "analyst"
    VIEWER = "viewer"


class Permission(str, Enum):
    """Defines specific permissions for actions within the system."""

    MANAGE_ORGANIZATION = "manage_organization"
    MANAGE_USERS = "manage_users"
    VIEW_DEALS = "view_deals"
    MANAGE_DEALS = "manage_deals"
    PERFORM_OUTREACH = "perform_outreach"


@dataclass
class User:
    """Represents a user within an organization."""

    user_id: str = field(default_factory=lambda: f"user_{uuid4()}")
    organization_id: str = ""
    email: str = ""
    hashed_password: str = ""  # Will store salt:hash
    role: str = Role.VIEWER.value


class AuthorizationService:
    """
    Phase 39: Manages role-based access control (RBAC).
    """

    def __init__(self):
        # Define which roles have which permissions
        self.role_permissions: Dict[str, Set[Permission]] = {
            Role.OWNER: {
                Permission.MANAGE_ORGANIZATION,
                Permission.MANAGE_USERS,
                Permission.MANAGE_DEALS,
                Permission.VIEW_DEALS,
                Permission.PERFORM_OUTREACH,
            },
            Role.ADMIN: {
                Permission.MANAGE_USERS,
                Permission.MANAGE_DEALS,
                Permission.VIEW_DEALS,
                Permission.PERFORM_OUTREACH,
            },
            Role.ACQUISITIONS: {Permission.MANAGE_DEALS, Permission.VIEW_DEALS, Permission.PERFORM_OUTREACH},
            Role.ANALYST: {Permission.VIEW_DEALS},
            Role.VIEWER: {Permission.VIEW_DEALS},
        }

    def can(self, user: User, permission: Permission, resource: Optional[Any] = None) -> bool:
        """Checks if a user has permission to perform an action, optionally on a resource."""
        # Check if the user's role has the required permission
        user_permissions = self.role_permissions.get(user.role, set())
        if permission not in user_permissions:
            return False

        # If a resource is provided, check for organization isolation
        if resource and hasattr(resource, "organization_id"):
            if user.organization_id != resource.organization_id:
                return False  # User is not in the same organization as the resource

        return True


@dataclass
class SaaSDashboardReport:
    """A structured report for the main SaaS dashboard."""

    organization_id: str
    market_heat: Dict[str, int] = field(default_factory=dict)
    top_deals: List[Dict[str, Any]] = field(default_factory=list)
    outreach_queue_count: int = 0
    learning_metrics: Dict[str, Any] = field(default_factory=dict)


class SaaSDashboard:
    """
    Phase 39: Generates a tenant-aware dashboard by connecting to existing services.
    """

    def __init__(
        self,
        user: User,
        pilot_runner: LivePilotRunner,
        pending_action_dashboard: PendingActionDashboard,
        validation_manager: ValidationManager,
    ):
        self.user = user
        self.pilot_runner = pilot_runner
        self.pending_action_dashboard = pending_action_dashboard
        self.validation_manager = validation_manager

    def generate_report(self, mock_opportunities: List[CanonicalProperty]) -> SaaSDashboardReport:
        """Generates a dashboard report for the user's organization."""
        pilot_report = self.pilot_runner.run(mock_opportunities)
        outreach_report = self.pending_action_dashboard.generate_report()
        metrics = self.validation_manager.generate_metrics()

        return SaaSDashboardReport(
            organization_id=self.user.organization_id,
            market_heat=pilot_report.market_ranking,
            top_deals=[deal.__dict__ for deal in pilot_report.top_ranked_opportunities[:3]],
            outreach_queue_count=len(outreach_report),
            learning_metrics=metrics.__dict__,
        )


@dataclass
class NotificationPreferences:
    """User-specific notification preferences."""

    user_id: str
    on_new_high_priority_deal: bool = True
    on_approval_request: bool = True
    on_deal_closed: bool = False


class UserConfigurationService:
    """
    Phase 39: Allows authorized users to manage system configurations.
    """

    def __init__(
        self,
        authz_service: AuthorizationService,
        scaling_manager: ScalingManager,
        # Other managers like a rule engine would be injected here
    ):
        self.authz_service = authz_service
        self.scaling_manager = scaling_manager
        self.notification_prefs: Dict[str, NotificationPreferences] = {}

    def configure_market(self, user: User, market_config: MarketConfig) -> bool:
        """Allows an authorized user to add or update a market configuration."""
        if not self.authz_service.can(user, Permission.MANAGE_ORGANIZATION):
            return False

        # Input validation
        if not market_config.market_id or not market_config.market_name:
            raise ValueError("Market ID and name are required.")

        self.scaling_manager.load_market_config(market_config)
        return True

    def set_notification_preferences(self, user: User, preferences: NotificationPreferences) -> bool:
        """Sets notification preferences for a user."""
        if user.user_id != preferences.user_id:
            return False  # A user can only set their own preferences

        self.notification_prefs[user.user_id] = preferences
        return True


class AuthenticationService:
    """
    Phase 39: Manages user registration, login, and password security.
    """

    def __init__(self, db_client: DatabaseClient):
        self.db_client = db_client

    def _hash_password(self, password: str, salt: Optional[bytes] = None) -> tuple[str, bytes]:
        """Hashes a password with a salt."""
        if salt is None:
            salt = secrets.token_bytes(16)
        pwd_hash = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
        return pwd_hash.hex(), salt

    def register_user(self, email: str, password: str, organization_id: str) -> Optional[User]:
        """Registers a new user, checking for duplicates first."""
        if self.db_client.find_user_by_email(email):
            return None  # User already exists

        hashed_password, salt = self._hash_password(password)
        password_storage = f"{salt.hex()}:{hashed_password}"

        user = User(organization_id=organization_id, email=email, hashed_password=password_storage)
        self.db_client.create_user(user)
        return user

    def login_user(self, email: str, password: str) -> Optional[User]:
        """Logs a user in by verifying their password."""
        user_data = self.db_client.find_user_by_email(email)
        if not user_data:
            return None

        try:
            salt_hex, stored_hash = user_data["hashed_password"].split(":")
            salt = bytes.fromhex(salt_hex)
            incoming_hash, _ = self._hash_password(password, salt)

            if secrets.compare_digest(stored_hash, incoming_hash):
                return User(**user_data)
        except (ValueError, TypeError):
            return None  # Handle malformed password storage
        return None