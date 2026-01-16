"""CRF Pydantic models based on the JSON Schema specification."""

from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

import yaml
from pydantic import BaseModel, ConfigDict, Field


# === Enums ===


class EntityType(str, Enum):
    """Types of context entities."""

    ORGANIZATION = "organization"
    SYSTEM = "system"
    POLICY = "policy"
    FACT = "fact"
    ARCHITECTURE = "architecture"
    CAPABILITY = "capability"


class RelationshipType(str, Enum):
    """Types of relationships between entities."""

    OWNS = "owns"
    OWNED_BY = "owned_by"
    DEPENDS_ON = "depends_on"
    DEPENDENCY_OF = "dependency_of"
    CONSTRAINS = "constrains"
    CONSTRAINED_BY = "constrained_by"
    INVALIDATES = "invalidates"
    INVALIDATED_BY = "invalidated_by"
    PART_OF = "part_of"
    CONTAINS = "contains"
    PRODUCES = "produces"
    PRODUCED_BY = "produced_by"
    RELATED_TO = "related_to"


# Organization Enums
class OrgType(str, Enum):
    COMPANY = "company"
    DIVISION = "division"
    DEPARTMENT = "department"
    TEAM = "team"
    SQUAD = "squad"
    WORKING_GROUP = "working_group"


class OrgSize(str, Enum):
    STARTUP = "startup"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    ENTERPRISE = "enterprise"


# System Enums
class SystemType(str, Enum):
    APPLICATION = "application"
    SERVICE = "service"
    PLATFORM = "platform"
    INFRASTRUCTURE = "infrastructure"
    DATABASE = "database"
    INTEGRATION = "integration"
    TOOL = "tool"


class SystemStatus(str, Enum):
    PLANNED = "planned"
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    DEPRECATED = "deprecated"
    DECOMMISSIONED = "decommissioned"


class Criticality(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class DataClassification(str, Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"


# Policy Enums
class PolicyType(str, Enum):
    GOVERNANCE = "governance"
    SECURITY = "security"
    COMPLIANCE = "compliance"
    ARCHITECTURAL = "architectural"
    OPERATIONAL = "operational"
    FINANCIAL = "financial"


class Enforcement(str, Enum):
    MANDATORY = "mandatory"
    RECOMMENDED = "recommended"
    ADVISORY = "advisory"


# Fact Enums
class FactType(str, Enum):
    CONTRACT = "contract"
    BUDGET = "budget"
    TIMELINE = "timeline"
    CONSTRAINT = "constraint"
    METRIC = "metric"
    EVENT = "event"
    STATUS = "status"


# Architecture Enums
class ArchitectureType(str, Enum):
    PATTERN = "pattern"
    PRINCIPLE = "principle"
    STANDARD = "standard"
    GUIDELINE = "guideline"
    REFERENCE = "reference"
    DECISION = "decision"


class Maturity(str, Enum):
    EMERGING = "emerging"
    ESTABLISHED = "established"
    MATURE = "mature"
    DECLINING = "declining"
    DEPRECATED = "deprecated"


class AdoptionStatus(str, Enum):
    PROPOSED = "proposed"
    PILOT = "pilot"
    ADOPTED = "adopted"
    STANDARD = "standard"
    RETIRING = "retiring"


# Capability Enums
class CapabilityType(str, Enum):
    SKILL = "skill"
    TOOL = "tool"
    PROCESS = "process"
    PRACTICE = "practice"
    CERTIFICATION = "certification"


class Proficiency(str, Enum):
    NONE = "none"
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class StrategicImportance(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# === Attribute Models ===


class OrganizationAttributes(BaseModel):
    """Attributes specific to organization entities."""

    model_config = ConfigDict(populate_by_name=True)

    org_type: OrgType | None = None
    size: OrgSize | None = None
    headcount: int | None = Field(None, ge=1)
    location: str | None = None
    industry: str | None = None
    compliance_frameworks: list[str] | None = None


class SystemAttributes(BaseModel):
    """Attributes specific to system entities."""

    model_config = ConfigDict(populate_by_name=True)

    system_type: SystemType | None = None
    status: SystemStatus | None = None
    criticality: Criticality | None = None
    technology_stack: list[str] | None = None
    hosting: str | None = None
    data_classification: DataClassification | None = None


class PolicyAttributes(BaseModel):
    """Attributes specific to policy entities."""

    model_config = ConfigDict(populate_by_name=True)

    policy_type: PolicyType | None = None
    enforcement: Enforcement | None = None
    scope: str | None = None
    rationale: str | None = None
    exceptions_process: str | None = None
    owner: str | None = None
    review_cycle: str | None = None


class FactAttributes(BaseModel):
    """Attributes specific to fact entities."""

    model_config = ConfigDict(populate_by_name=True)

    fact_type: FactType | None = None
    value: str | int | float | bool | dict[str, Any] | None = None
    unit: str | None = None
    confidence: int | None = Field(None, ge=0, le=100)
    source_reference: str | None = None
    verified: bool | None = None
    verified_at: datetime | None = None


class ArchitectureAttributes(BaseModel):
    """Attributes specific to architecture entities."""

    model_config = ConfigDict(populate_by_name=True)

    architecture_type: ArchitectureType | None = None
    domain: str | None = None
    maturity: Maturity | None = None
    adoption_status: AdoptionStatus | None = None
    alternatives: list[str] | None = None


class CapabilityAttributes(BaseModel):
    """Attributes specific to capability entities."""

    model_config = ConfigDict(populate_by_name=True)

    capability_type: CapabilityType | None = None
    proficiency: Proficiency | None = None
    coverage: int | None = Field(None, ge=0, le=100)
    training_available: bool | None = None
    strategic_importance: StrategicImportance | None = None


# === Sub-Models ===


class Validity(BaseModel):
    """Temporal bounds for when context is valid."""

    model_config = ConfigDict(populate_by_name=True)

    valid_from: datetime | None = None
    valid_until: datetime | None = None


class CRFRelationship(BaseModel):
    """Edge to another entity in the context graph."""

    model_config = ConfigDict(populate_by_name=True)

    target_id: UUID
    type: RelationshipType
    description: str | None = None


class Supersedes(BaseModel):
    """Reference to entity this one replaces."""

    model_config = ConfigDict(populate_by_name=True)

    entity_id: UUID
    reason: str | None = None
    superseded_at: datetime | None = None


class Provenance(BaseModel):
    """Origin and authorship information."""

    model_config = ConfigDict(populate_by_name=True)

    source: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str | None = None
    updated_at: datetime | None = None
    updated_by: str | None = None


# Type alias for attributes union
EntityAttributes = (
    OrganizationAttributes
    | SystemAttributes
    | PolicyAttributes
    | FactAttributes
    | ArchitectureAttributes
    | CapabilityAttributes
)


# === Main Entity ===


class Entity(BaseModel):
    """A node in the context knowledge graph."""

    model_config = ConfigDict(populate_by_name=True)

    id: UUID = Field(default_factory=uuid4)
    type: EntityType
    name: str = Field(..., min_length=1, max_length=200)
    description: str | None = None
    attributes: EntityAttributes | None = None
    validity: Validity | None = None
    relationships: list[CRFRelationship] | None = None
    supersedes: Supersedes | None = None
    provenance: Provenance | None = None
    tags: list[str] | None = None

    # === Builder Methods ===

    def add_relationship(
        self,
        target_id: UUID,
        rel_type: RelationshipType | str,
        description: str | None = None,
    ) -> "Entity":
        """Add a relationship to another entity."""
        if isinstance(rel_type, str):
            rel_type = RelationshipType(rel_type)
        if self.relationships is None:
            self.relationships = []
        self.relationships.append(
            CRFRelationship(target_id=target_id, type=rel_type, description=description)
        )
        return self

    def set_validity(
        self,
        valid_from: datetime | None = None,
        valid_until: datetime | None = None,
    ) -> "Entity":
        """Set temporal validity bounds."""
        self.validity = Validity(valid_from=valid_from, valid_until=valid_until)
        return self

    def supersede(
        self,
        previous_entity_id: UUID,
        reason: str | None = None,
    ) -> "Entity":
        """Mark this entity as superseding another."""
        self.supersedes = Supersedes(
            entity_id=previous_entity_id,
            reason=reason,
            superseded_at=datetime.utcnow(),
        )
        return self


# === Root Document ===


class ContextDocument(BaseModel):
    """A complete CRF Context Document."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    crf_version: str = "0.1.0"
    entity: Entity

    # === Factory Methods ===

    @classmethod
    def create_organization(
        cls,
        name: str,
        description: str | None = None,
        **attributes: Any,
    ) -> "ContextDocument":
        """Create an organization context document."""
        return cls(
            entity=Entity(
                type=EntityType.ORGANIZATION,
                name=name,
                description=description,
                attributes=OrganizationAttributes(**attributes) if attributes else None,
                provenance=Provenance(source="manual"),
            )
        )

    @classmethod
    def create_system(
        cls,
        name: str,
        description: str | None = None,
        **attributes: Any,
    ) -> "ContextDocument":
        """Create a system context document."""
        return cls(
            entity=Entity(
                type=EntityType.SYSTEM,
                name=name,
                description=description,
                attributes=SystemAttributes(**attributes) if attributes else None,
                provenance=Provenance(source="manual"),
            )
        )

    @classmethod
    def create_policy(
        cls,
        name: str,
        description: str | None = None,
        **attributes: Any,
    ) -> "ContextDocument":
        """Create a policy context document."""
        return cls(
            entity=Entity(
                type=EntityType.POLICY,
                name=name,
                description=description,
                attributes=PolicyAttributes(**attributes) if attributes else None,
                provenance=Provenance(source="manual"),
            )
        )

    @classmethod
    def create_fact(
        cls,
        name: str,
        value: Any,
        fact_type: FactType | str = FactType.STATUS,
        description: str | None = None,
    ) -> "ContextDocument":
        """Create a fact context document."""
        if isinstance(fact_type, str):
            fact_type = FactType(fact_type)
        return cls(
            entity=Entity(
                type=EntityType.FACT,
                name=name,
                description=description,
                attributes=FactAttributes(fact_type=fact_type, value=value),
                provenance=Provenance(source="manual"),
            )
        )

    @classmethod
    def create_architecture(
        cls,
        name: str,
        description: str | None = None,
        **attributes: Any,
    ) -> "ContextDocument":
        """Create an architecture context document."""
        return cls(
            entity=Entity(
                type=EntityType.ARCHITECTURE,
                name=name,
                description=description,
                attributes=ArchitectureAttributes(**attributes) if attributes else None,
                provenance=Provenance(source="manual"),
            )
        )

    @classmethod
    def create_capability(
        cls,
        name: str,
        description: str | None = None,
        **attributes: Any,
    ) -> "ContextDocument":
        """Create a capability context document."""
        return cls(
            entity=Entity(
                type=EntityType.CAPABILITY,
                name=name,
                description=description,
                attributes=CapabilityAttributes(**attributes) if attributes else None,
                provenance=Provenance(source="manual"),
            )
        )

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
    def load(cls, path: str | Path) -> "ContextDocument":
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
    def from_yaml(cls, content: str) -> "ContextDocument":
        """Parse from YAML string."""
        data = yaml.safe_load(content)
        return cls.model_validate(data)

    @classmethod
    def from_json(cls, content: str) -> "ContextDocument":
        """Parse from JSON string."""
        import json

        data = json.loads(content)
        return cls.model_validate(data)
