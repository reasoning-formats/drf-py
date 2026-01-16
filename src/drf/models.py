"""DRF Pydantic models based on the JSON Schema specification."""

from datetime import date, datetime
from enum import Enum
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

import yaml
from pydantic import BaseModel, ConfigDict, EmailStr, Field


# === Enums ===


class CognitivePhase(str, Enum):
    """Linear progression of decision-making phases."""

    EXPLORATION = "exploration"
    ANALYSIS = "analysis"
    SYNTHESIS = "synthesis"
    DECISION = "decision"


class ReasoningPattern(str, Enum):
    """Enumerated reasoning patterns organized into categories."""

    # Analytical
    OPERATIONAL = "operational"
    RISK_BASED = "risk_based"
    CONTRAFACTUAL = "contrafactual"
    COMPARATIVE = "comparative"
    COST_BENEFIT = "cost_benefit"
    # Cognitive
    INTUITIVE = "intuitive"
    DELIBERATIVE = "deliberative"
    HEURISTIC = "heuristic"
    SYSTEMATIC = "systematic"
    CREATIVE = "creative"
    # Decision
    CONSENSUS = "consensus"
    AUTHORITY = "authority"
    DELEGATION = "delegation"
    VOTING = "voting"
    ESCALATION = "escalation"


class InterventionType(str, Enum):
    """Categories of interventions that shape reasoning."""

    QUESTION = "question"
    CHALLENGE = "challenge"
    CONSTRAINT = "constraint"
    INSIGHT = "insight"
    EXTERNAL_INPUT = "external_input"


class Impact(str, Enum):
    """Severity levels for tensions and risks."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class DecisionStatus(str, Enum):
    """Lifecycle status of a decision."""

    DRAFT = "draft"
    REVIEW = "review"
    APPROVED = "approved"
    REJECTED = "rejected"
    SUPERSEDED = "superseded"
    ARCHIVED = "archived"


class Priority(str, Enum):
    """Priority levels for objectives."""

    MUST_HAVE = "must_have"
    SHOULD_HAVE = "should_have"
    NICE_TO_HAVE = "nice_to_have"


class Role(str, Enum):
    """Roles of actors in a decision."""

    AUTHOR = "author"
    REVIEWER = "reviewer"
    APPROVER = "approver"
    CONTRIBUTOR = "contributor"
    STAKEHOLDER = "stakeholder"


class Relationship(str, Enum):
    """Types of relationships between decisions."""

    SUPERSEDES = "supersedes"
    SUPERSEDED_BY = "superseded_by"
    DEPENDS_ON = "depends_on"
    DEPENDENCY_OF = "dependency_of"
    RELATED_TO = "related_to"
    CONFLICTS_WITH = "conflicts_with"


class ValidationStatus(str, Enum):
    """Result of validating a decision against context."""

    SATISFIED = "satisfied"
    VIOLATED = "violated"
    ACKNOWLEDGED = "acknowledged"
    NOT_APPLICABLE = "not_applicable"


class ContextEntityType(str, Enum):
    """Types of CRF context entities."""

    ORGANIZATION = "organization"
    SYSTEM = "system"
    POLICY = "policy"
    FACT = "fact"
    ARCHITECTURE = "architecture"
    CAPABILITY = "capability"


class ContextAction(str, Enum):
    """Actions a decision can take on context."""

    CREATES = "creates"
    UPDATES = "updates"
    INVALIDATES = "invalidates"


# === Sub-models ===


class Constraint(BaseModel):
    """A hard constraint that must be satisfied."""

    model_config = ConfigDict(populate_by_name=True)

    description: str
    source: str | None = None
    negotiable: bool = False


class Objective(BaseModel):
    """A goal or success criterion."""

    model_config = ConfigDict(populate_by_name=True)

    description: str
    priority: Priority | None = None
    measurable: bool = False


class Environment(BaseModel):
    """Relevant environmental factors."""

    model_config = ConfigDict(populate_by_name=True)

    technical: str | None = None
    organizational: str | None = None
    temporal: str | None = None


class RelatedDecision(BaseModel):
    """Reference to a related decision."""

    model_config = ConfigDict(populate_by_name=True)

    id: UUID
    relationship: Relationship
    description: str | None = None


class Intervention(BaseModel):
    """A question, challenge, or input that shaped reasoning."""

    model_config = ConfigDict(populate_by_name=True)

    id: str
    type: InterventionType
    content: str
    source: str | None = None
    timestamp: datetime | None = None
    impact: str | None = None


class Assumption(BaseModel):
    """An explicit or implicit premise accepted during the decision."""

    model_config = ConfigDict(populate_by_name=True)

    description: str
    validated: bool
    confidence: int | None = Field(None, ge=0, le=100)
    source: str | None = None


class Tension(BaseModel):
    """A known trade-off or risk left open or accepted."""

    model_config = ConfigDict(populate_by_name=True)

    description: str
    impact: Impact
    mitigation: str | None = None
    accepted_by: str | None = None


class FollowUp(BaseModel):
    """A next step or action required."""

    model_config = ConfigDict(populate_by_name=True)

    action: str
    owner: str | None = None
    due_date: date | None = None


class Alternative(BaseModel):
    """A ranked alternative outcome."""

    model_config = ConfigDict(populate_by_name=True)

    decision: str
    rationale_against: str
    conditions_for_reconsideration: str | None = None


class Actor(BaseModel):
    """A person or system involved in the decision."""

    model_config = ConfigDict(populate_by_name=True)

    name: str
    role: Role
    email: EmailStr | None = None


class ContextRef(BaseModel):
    """Reference to a CRF entity for validation."""

    model_config = ConfigDict(populate_by_name=True)

    context_id: UUID
    context_type: ContextEntityType
    context_name: str | None = None
    validation_status: ValidationStatus
    advisory_notes: str | None = None


class ContextOutput(BaseModel):
    """A CRF entity this decision creates, updates, or invalidates."""

    model_config = ConfigDict(populate_by_name=True)

    action: ContextAction
    entity_type: ContextEntityType
    entity_id: UUID | None = None
    entity_data: dict[str, Any] | None = None
    reason: str | None = None


# === Main Components ===


class DecisionIdentity(BaseModel):
    """Core identity and intent of the decision."""

    model_config = ConfigDict(populate_by_name=True)

    id: UUID = Field(default_factory=uuid4)
    title: str = Field(..., min_length=1, max_length=200)
    domain: str | None = None
    intent: str = Field(..., min_length=1)
    related_decisions: list[RelatedDecision] | None = None


class Context(BaseModel):
    """Environmental and situational context for the decision."""

    model_config = ConfigDict(populate_by_name=True)

    constraints: list[Constraint] = Field(default_factory=list)
    objectives: list[Objective] = Field(default_factory=list)
    environment: Environment | None = None


class CognitiveState(BaseModel):
    """Current phase and confidence of the decision process."""

    model_config = ConfigDict(populate_by_name=True)

    phase: CognitivePhase
    confidence: int = Field(..., ge=0, le=100)
    phase_notes: str | None = None


class Reasoning(BaseModel):
    """Explicit reasoning patterns applied during the decision."""

    model_config = ConfigDict(populate_by_name=True)

    patterns_applied: list[ReasoningPattern] | None = None
    notes: str | None = None


class Synthesis(BaseModel):
    """The consolidated decision outcome."""

    model_config = ConfigDict(populate_by_name=True)

    decision: str
    rationale: str
    follow_ups: list[FollowUp] | None = None
    alternatives: list[Alternative] | None = None


class ContextValidation(BaseModel):
    """Links this decision to CRF entities for validation."""

    model_config = ConfigDict(populate_by_name=True)

    validated_at: datetime | None = None
    context_refs: list[ContextRef] | None = None
    context_outputs: list[ContextOutput] | None = None


class Meta(BaseModel):
    """Metadata about the decision document."""

    model_config = ConfigDict(populate_by_name=True)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime | None = None
    status: DecisionStatus = DecisionStatus.DRAFT
    actors: list[Actor] | None = None
    source: str | None = None
    tags: list[str] | None = None


# === Root Document ===


class DecisionDocument(BaseModel):
    """A complete DRF Decision Document."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    drf_version: str = "0.1.0"
    decision: DecisionIdentity
    context: Context
    cognitive_state: CognitiveState
    reasoning: Reasoning | None = None
    interventions: list[Intervention] | None = None
    assumptions: list[Assumption] | None = None
    unresolved_tensions: list[Tension] | None = None
    synthesis: Synthesis
    context_validation: ContextValidation | None = None
    meta: Meta = Field(default_factory=Meta)

    # === Factory Methods ===

    @classmethod
    def create(
        cls,
        title: str,
        intent: str,
        domain: str | None = None,
    ) -> "DecisionDocument":
        """Create a new decision document with minimal required fields."""
        return cls(
            decision=DecisionIdentity(title=title, intent=intent, domain=domain),
            context=Context(),
            cognitive_state=CognitiveState(phase=CognitivePhase.EXPLORATION, confidence=0),
            synthesis=Synthesis(decision="", rationale=""),
        )

    # === Builder Methods ===

    def add_constraint(
        self,
        description: str,
        source: str | None = None,
        negotiable: bool = False,
    ) -> "DecisionDocument":
        """Add a constraint to the context."""
        self.context.constraints.append(
            Constraint(description=description, source=source, negotiable=negotiable)
        )
        return self

    def add_objective(
        self,
        description: str,
        priority: Priority | None = None,
        measurable: bool = False,
    ) -> "DecisionDocument":
        """Add an objective to the context."""
        self.context.objectives.append(
            Objective(description=description, priority=priority, measurable=measurable)
        )
        return self

    def set_phase(self, phase: CognitivePhase | str, confidence: int) -> "DecisionDocument":
        """Set the cognitive phase and confidence."""
        if isinstance(phase, str):
            phase = CognitivePhase(phase)
        self.cognitive_state = CognitiveState(phase=phase, confidence=confidence)
        return self

    def add_reasoning_pattern(self, pattern: ReasoningPattern | str) -> "DecisionDocument":
        """Add a reasoning pattern."""
        if isinstance(pattern, str):
            pattern = ReasoningPattern(pattern)
        if self.reasoning is None:
            self.reasoning = Reasoning(patterns_applied=[])
        if self.reasoning.patterns_applied is None:
            self.reasoning.patterns_applied = []
        self.reasoning.patterns_applied.append(pattern)
        return self

    def add_assumption(
        self,
        description: str,
        validated: bool = False,
        confidence: int | None = None,
    ) -> "DecisionDocument":
        """Add an assumption."""
        if self.assumptions is None:
            self.assumptions = []
        self.assumptions.append(
            Assumption(description=description, validated=validated, confidence=confidence)
        )
        return self

    def add_tension(
        self,
        description: str,
        impact: Impact | str,
        mitigation: str | None = None,
    ) -> "DecisionDocument":
        """Add an unresolved tension."""
        if isinstance(impact, str):
            impact = Impact(impact)
        if self.unresolved_tensions is None:
            self.unresolved_tensions = []
        self.unresolved_tensions.append(
            Tension(description=description, impact=impact, mitigation=mitigation)
        )
        return self

    def synthesize(
        self,
        decision: str,
        rationale: str,
    ) -> "DecisionDocument":
        """Set the synthesis decision and rationale."""
        self.synthesis = Synthesis(decision=decision, rationale=rationale)
        self.cognitive_state.phase = CognitivePhase.DECISION
        return self

    def add_alternative(
        self,
        decision: str,
        rationale_against: str,
    ) -> "DecisionDocument":
        """Add a rejected alternative."""
        if self.synthesis.alternatives is None:
            self.synthesis.alternatives = []
        self.synthesis.alternatives.append(
            Alternative(decision=decision, rationale_against=rationale_against)
        )
        return self

    def approve(self, approver: str) -> "DecisionDocument":
        """Mark the decision as approved."""
        self.meta.status = DecisionStatus.APPROVED
        self.meta.updated_at = datetime.utcnow()
        if self.meta.actors is None:
            self.meta.actors = []
        self.meta.actors.append(Actor(name=approver, role=Role.APPROVER))
        return self

    # === Serialization ===

    def to_yaml(self) -> str:
        """Serialize to YAML string."""
        data = self.model_dump(mode="json", exclude_none=True)
        return yaml.dump(data, default_flow_style=False, sort_keys=False, allow_unicode=True)

    def to_json(self) -> str:
        """Serialize to JSON string."""
        return self.model_dump_json(indent=2, exclude_none=True)

    def save(self, path: str | Path) -> None:
        """Save to file (YAML or JSON based on extension)."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        content = self.to_yaml() if path.suffix in (".yaml", ".yml") else self.to_json()
        path.write_text(content)

    @classmethod
    def load(cls, path: str | Path) -> "DecisionDocument":
        """Load from file (YAML or JSON)."""
        path = Path(path)
        content = path.read_text()
        if path.suffix in (".yaml", ".yml"):
            data = yaml.safe_load(content)
        else:
            import json

            data = json.loads(content)
        return cls.model_validate(data)

    @classmethod
    def from_yaml(cls, content: str) -> "DecisionDocument":
        """Parse from YAML string."""
        data = yaml.safe_load(content)
        return cls.model_validate(data)

    @classmethod
    def from_json(cls, content: str) -> "DecisionDocument":
        """Parse from JSON string."""
        import json

        data = json.loads(content)
        return cls.model_validate(data)
