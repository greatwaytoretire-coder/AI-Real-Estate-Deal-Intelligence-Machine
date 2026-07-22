"""AI Real Estate Deal Intelligence Machine package."""

from .audit_logger import AuditLogger
from .config import settings
from .db_client import DatabaseClient
from .phase0 import MissionControlDashboard, MockProviderRegistry
from .phase1 import FoundationApp
from .phase2 import (
    CSVImportProvider,
    IngestionEngine as IngestionEngineV2,
    IngestionEvent,
    MockBuyerProvider as MockBuyerProviderV2,
    MockGovernmentProvider,
    MockMarketProvider as MockMarketProviderV2,
    MockPropertyProvider as MockPropertyProviderV2,
    MockTransactionProvider,
    ProviderHealth,
    ProviderRegistry as ProviderRegistryV2,
    ProviderStatus,
    ProviderSyncSchedule,
)
from .phase3 import HeatMapEngine, MarketAlertSystem, MarketIntelligenceAgent, MarketScore, MarketSnapshot
from .phase4 import DealCandidate, PropertyDiscoveryAgent, PropertyEvent, PropertyProfile
from .phase5 import DealScorecard, OpportunityScoringEngine, PriorityDealQueue
from .phase6 import ARVEstimate, ARVAgent, ComparableSalesAgent, RepairEstimate, RepairEstimationAgent, RepairItem
from .phase7 import DealUnderwritingAgent, UnderwritingEvent, UnderwritingResult
from .phase8 import DealRiskAgent, RiskAssessment
from .phase9 import (
    BuyerActivityProfile,
    BuyerIntelligenceEngine,
    BuyerIntelligenceEvent,
    BuyerMatchScore,
    BuyerProfile,
    BuyerReliabilityScore,
)
from .phase10 import BuyerMatchOpportunity, BuyerMatchingEngine, BuyerRankedMatch
from .phase11 import SellerAcquisitionAgent, SellerOpportunity, SellerQualificationPlan, SellerStage
from .phase12 import BuyerDispositionAgent, BuyerDispositionSummary, BuyerInterestClassification
from .phase13 import DealRoom, DealRoomAccess, DealRoomAgent, DealRoomMetrics
from .phase14 import DealLifecycleStage, DealLifecycleWorkflow, NextBestActionEngine
from .phase15 import LearningVersion, OutcomeLearningEngine, OutcomePerformanceReport
from .phase16 import MachineStatus, MissionControlDashboard as Phase16MissionControlDashboard, MissionControlMetrics
from .phase17 import RuleAction, RuleCondition, WorkflowConfigurationEngine, WorkflowRule
from .phase18 import ComplianceAuditTrail, ComplianceGuardrailAgent, GuardrailDecision
from .phase19 import EndToEndSimulationEngine, SimulationEvent, SimulationResult
from .phase20 import EmergencyStopControls, MachineHealthMonitor, ProductionDeploymentAgent
from .phase23 import EndToEndDealSimulation, EndToEndSimulationReport
from .phase24 import (
    DataSourceType,
    MarketPilotConfig,
    PilotDashboard,
    PilotDataRecord,
)
from .phase25 import (
    ActionForApproval,
    ApprovalStatus,
    AuditEntry,
    HumanInTheLoopEngine,
    PendingActionDashboard,
)
from .phase26 import (
    AttomApiProvider,
    DataProvider,
    MockAttomProvider,
    ProviderConfig,
    ProviderManager,
)
from .phase27 import (
    AccuracyReport,
    DealValidationEngine,
    ValidatedDeal,
    ValidationStatus,
)
from .phase28 import (
    AutonomyLevel,
    ReliabilityEngine,
    SafetyControls,
    SystemState,
    Job,
)
from .phase29 import (
    MarketConfig as ScalingMarketConfig, # Alias to avoid name clash
    ScalingManager,
    MarketUsage,
)
from .phase30 import (
    CanonicalProperty,
    ContinuousRuntime,
    DeduplicationEngine,
    IngestionRun,
    JobStatus,
    NormalizationEngine,
    OperatingMode,
    RuntimeEvent,
    RuntimeJobQueue,
    Worker,
)
from .phase31 import (
    AttomDataDownloader,
    LiveDataProvider,
)
from .phase32 import (
    LivePilotConfig,
    LivePilotRunner,
    MarketRankingEngine,
    PilotReport,
)
from .phase33 import (
    AIPrediction,
    ActualOutcome,
    LearningRecord,
    ValidationResult,
)
from .phase34 import (
    BuyerActivity,
    BuyerContactInfo,
    BuyerInvestmentCriteria,
    EnhancedBuyerProfile,
    BuyerStrategyClassification,
    BuyerStrategyClassifier,
    BuyerReliabilityScore,
    BuyerReliabilityScorer,
    DealContext,
    BuyerMatchResult,
    BuyerDealMatcher,
)
from .phase35 import (
    CommunicationContentAgent,
    OutreachDraft,
    OutreachOrchestrationAgent,
    ContactProtectionService,
    ActionExecutionAgent,
    CommunicationProvider,
    MockCommunicationProvider,
)
from .phase36 import (
    AIAgent,
    AgentContract,
    AgentInput,
    AgentOutput,
    AgentWorkflow,
    AgentOrchestrator,
)
from .phase37 import (
    MultiMarketOrchestrator,
    MultiMarketReport,
)
from .phase38 import (
    LearningPipelineOrchestrator,
    ModelImprovementProposal,
    ModelRegistry,
    ModelVersion,
    ModelVersionStatus,
)
from .phase39 import (
    AuthenticationService,
    Organization,
    User,
    AuthorizationService,
    Permission,
    Role,
    SaaSDashboard,
    SaaSDashboardReport,
    UserConfigurationService,
    NotificationPreferences,
)
from .integration_harness import EndToEndIntegrationHarness
from .provider_registry import ProviderRegistry

__all__ = [
    "MissionControlDashboard",
    "MockProviderRegistry",
    "ProviderRegistryV2",
    "ProviderRegistry",
    "FoundationApp",
    "DatabaseClient",
    "AuditLogger",
    "settings",
    "DealRiskAgent",
    "RiskAssessment",
    "IngestionEvent",
    "IngestionEngineV2",
    "ProviderHealth",
    "ProviderStatus",
    "ProviderSyncSchedule",
    "CSVImportProvider",
    "MockPropertyProviderV2",
    "MockBuyerProviderV2",
    "MockMarketProviderV2",
    "MockTransactionProvider",
    "MockGovernmentProvider",
    "MarketScore",
    "MarketSnapshot",
    "MarketIntelligenceAgent",
    "HeatMapEngine",
    "MarketAlertSystem",
    "PropertyProfile",
    "PropertyEvent",
    "DealCandidate",
    "PropertyDiscoveryAgent",
    "DealScorecard",
    "PriorityDealQueue",
    "OpportunityScoringEngine",
    "ARVEstimate", "RepairItem", "RepairEstimate", "ComparableSalesAgent", "ARVAgent", "RepairEstimationAgent", "UnderwritingEvent", "UnderwritingResult", "DealUnderwritingAgent",
    "BuyerProfile",
    "BuyerActivityProfile",
    "BuyerMatchScore",
    "BuyerReliabilityScore",
    "BuyerIntelligenceEvent",
    "BuyerIntelligenceEngine",
    "BuyerMatchOpportunity",
    "BuyerRankedMatch",
    "BuyerMatchingEngine",
    "SellerStage",
    "SellerOpportunity",
    "SellerQualificationPlan",
    "SellerAcquisitionAgent",
    "BuyerDispositionSummary",
    "BuyerInterestClassification",
    "BuyerDispositionAgent",
    "DealRoom",
    "DealRoomAccess",
    "DealRoomMetrics",
    "DealRoomAgent",
    "DealLifecycleStage",
    "DealLifecycleWorkflow",
    "NextBestActionEngine",
    "OutcomePerformanceReport",
    "LearningVersion",
    "OutcomeLearningEngine",
    "MachineStatus",
    "Phase16MissionControlDashboard",
    "MissionControlMetrics",
    "RuleCondition",
    "RuleAction",
    "WorkflowRule",
    "WorkflowConfigurationEngine",
    "GuardrailDecision",
    "ComplianceAuditTrail",
    "ComplianceGuardrailAgent",
    "SimulationEvent",
    "SimulationResult",
    "EndToEndSimulationEngine",
    "EmergencyStopControls",
    "MachineHealthMonitor",
    "ProductionDeploymentAgent",
    "EndToEndDealSimulation",
    "EndToEndSimulationReport",
    "MarketPilotConfig",
    "PilotDataRecord",
    "DataSourceType",
    "PilotDashboard",
    "ActionForApproval",
    "ApprovalStatus",
    "AuditEntry",
    "HumanInTheLoopEngine",
    "PendingActionDashboard",
    "DataProvider",
    "ProviderConfig",
    "ProviderManager",
    "AttomApiProvider",
    "MockAttomProvider",
    "DealValidationEngine",
    "ValidatedDeal",
    "ValidationStatus",
    "AccuracyReport",
    "AutonomyLevel",
    "SystemState",
    "ReliabilityEngine",
    "SafetyControls",
    "Job",
    "ScalingMarketConfig",
    "ScalingManager",
    "MarketUsage",
    "EndToEndIntegrationHarness",
    "ContinuousRuntime",
    "OperatingMode",
    "IngestionRun",
    "CanonicalProperty",
    "RuntimeEvent",
    "JobStatus",
    "DeduplicationEngine",
    "NormalizationEngine",
    "RuntimeJobQueue",
    "Worker",
    "LiveDataProvider",
    "AttomDataDownloader",
]
__all__.extend([
    "LivePilotConfig",
    "LivePilotRunner",
    "MarketRankingEngine",
    "PilotReport",
    "AIPrediction",
    "ActualOutcome",
    "ValidationResult",
    "LearningRecord",
    "EnhancedBuyerProfile",
    "BuyerInvestmentCriteria",
    "BuyerActivity",
    "BuyerContactInfo",
    "BuyerStrategyClassification",
    "BuyerStrategyClassifier",
    "BuyerReliabilityScore",
    "BuyerReliabilityScorer",
    "DealContext",
    "BuyerMatchResult",
    "BuyerDealMatcher",
    "CommunicationContentAgent",
    "OutreachDraft",
    "OutreachOrchestrationAgent",
    "ContactProtectionService",
    "ActionExecutionAgent",
    "CommunicationProvider",
    "MockCommunicationProvider",
    "AIAgent",
    "AgentContract",
    "AgentInput",
    "AgentOutput",
    "AgentWorkflow",
    "AgentOrchestrator",
    "MultiMarketOrchestrator",
    "MultiMarketReport",
    "LearningPipelineOrchestrator",
    "ModelImprovementProposal",
    "ModelRegistry",
    "ModelVersion",
    "ModelVersionStatus",
    "AuthenticationService",
    "User",
    "Organization",
    "AuthorizationService",
    "Permission",
    "Role",
    "SaaSDashboard",
    "SaaSDashboardReport",
    "UserConfigurationService",
    "NotificationPreferences",
])
