"""Tests for CRF models."""

import tempfile
from pathlib import Path
from uuid import uuid4

import pytest

from crf import (
    ContextDocument,
    Criticality,
    Enforcement,
    EntityType,
    FactType,
    OrgType,
    PolicyType,
    RelationshipType,
    SystemStatus,
    SystemType,
)


class TestContextDocument:
    """Tests for ContextDocument model."""

    def test_create_organization(self):
        """Test creating an organization context."""
        doc = ContextDocument.create_organization(
            name="ACME Corp",
            description="A software company",
            org_type=OrgType.COMPANY,
            headcount=150,
            industry="Technology",
        )

        assert doc.entity.name == "ACME Corp"
        assert doc.entity.type == EntityType.ORGANIZATION
        assert doc.entity.attributes.org_type == OrgType.COMPANY
        assert doc.entity.attributes.headcount == 150

    def test_create_system(self):
        """Test creating a system context."""
        doc = ContextDocument.create_system(
            name="Production API",
            description="Main API gateway",
            system_type=SystemType.SERVICE,
            status=SystemStatus.PRODUCTION,
            criticality=Criticality.HIGH,
            technology_stack=["Python", "FastAPI", "PostgreSQL"],
        )

        assert doc.entity.name == "Production API"
        assert doc.entity.type == EntityType.SYSTEM
        assert doc.entity.attributes.system_type == SystemType.SERVICE
        assert doc.entity.attributes.status == SystemStatus.PRODUCTION
        assert "Python" in doc.entity.attributes.technology_stack

    def test_create_policy(self):
        """Test creating a policy context."""
        doc = ContextDocument.create_policy(
            name="No Kubernetes Migration",
            description="Moratorium on K8s adoption until Q4 2024",
            policy_type=PolicyType.ARCHITECTURAL,
            enforcement=Enforcement.MANDATORY,
            scope="All production systems",
        )

        assert doc.entity.name == "No Kubernetes Migration"
        assert doc.entity.type == EntityType.POLICY
        assert doc.entity.attributes.policy_type == PolicyType.ARCHITECTURAL
        assert doc.entity.attributes.enforcement == Enforcement.MANDATORY

    def test_create_fact(self):
        """Test creating a fact context."""
        doc = ContextDocument.create_fact(
            name="Annual Cloud Budget",
            value=500000,
            fact_type=FactType.BUDGET,
            description="Maximum cloud spend for FY2024",
        )

        assert doc.entity.name == "Annual Cloud Budget"
        assert doc.entity.type == EntityType.FACT
        assert doc.entity.attributes.fact_type == FactType.BUDGET
        assert doc.entity.attributes.value == 500000

    def test_add_relationship(self):
        """Test adding relationships between entities."""
        target_id = uuid4()
        doc = ContextDocument.create_system(name="API Gateway")

        doc.entity.add_relationship(
            target_id=target_id,
            rel_type=RelationshipType.DEPENDS_ON,
            description="Requires database for persistence",
        )

        assert len(doc.entity.relationships) == 1
        assert doc.entity.relationships[0].target_id == target_id
        assert doc.entity.relationships[0].type == RelationshipType.DEPENDS_ON

    def test_supersession(self):
        """Test marking an entity as superseding another."""
        old_id = uuid4()
        doc = ContextDocument.create_policy(
            name="Updated Security Policy v2",
        )

        doc.entity.supersede(
            previous_entity_id=old_id,
            reason="Updated to address new compliance requirements",
        )

        assert doc.entity.supersedes is not None
        assert doc.entity.supersedes.entity_id == old_id
        assert "compliance" in doc.entity.supersedes.reason

    def test_yaml_serialization(self):
        """Test YAML serialization roundtrip."""
        original = ContextDocument.create_organization(
            name="Test Org",
            description="For testing",
        )

        yaml_str = original.to_yaml()
        assert "crf_version:" in yaml_str
        assert "Test Org" in yaml_str

        restored = ContextDocument.from_yaml(yaml_str)
        assert restored.entity.name == original.entity.name
        assert restored.entity.type == original.entity.type

    def test_json_serialization(self):
        """Test JSON serialization roundtrip."""
        original = ContextDocument.create_system(
            name="Test System",
            system_type=SystemType.APPLICATION,
        )

        json_str = original.to_json()
        assert '"crf_version":' in json_str
        assert '"Test System"' in json_str

        restored = ContextDocument.from_json(json_str)
        assert restored.entity.name == original.entity.name
        assert restored.entity.type == original.entity.type

    def test_file_save_and_load(self):
        """Test saving and loading from files."""
        original = ContextDocument.create_policy(
            name="Test Policy",
            policy_type=PolicyType.GOVERNANCE,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            # Test YAML
            yaml_path = Path(tmpdir) / "context.yaml"
            original.save(yaml_path)
            assert yaml_path.exists()

            loaded = ContextDocument.load(yaml_path)
            assert loaded.entity.name == original.entity.name

            # Test JSON
            json_path = Path(tmpdir) / "context.json"
            original.save(json_path)
            assert json_path.exists()

            loaded = ContextDocument.load(json_path)
            assert loaded.entity.name == original.entity.name

    def test_uuid_generation(self):
        """Test that UUIDs are auto-generated."""
        doc = ContextDocument.create_organization(name="Test")

        assert doc.entity.id is not None
        assert len(str(doc.entity.id)) == 36
