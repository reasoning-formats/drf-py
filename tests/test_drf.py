"""Tests for DRF models."""

import tempfile
from pathlib import Path

import pytest

from drf import (
    CognitivePhase,
    DecisionDocument,
    DecisionStatus,
    Impact,
    Priority,
    ReasoningPattern,
)


class TestDecisionDocument:
    """Tests for DecisionDocument model."""

    def test_create_minimal_decision(self):
        """Test creating a decision with minimal required fields."""
        doc = DecisionDocument.create(
            title="Test Decision",
            intent="Test what happens when we do X",
        )

        assert doc.decision.title == "Test Decision"
        assert doc.decision.intent == "Test what happens when we do X"
        assert doc.cognitive_state.phase == CognitivePhase.EXPLORATION
        assert doc.cognitive_state.confidence == 0
        assert doc.meta.status == DecisionStatus.DRAFT

    def test_builder_pattern(self):
        """Test fluent builder pattern."""
        doc = (
            DecisionDocument.create(
                title="Use PostgreSQL",
                intent="Select primary database",
                domain="architecture",
            )
            .add_constraint("Must support ACID", source="regulatory", negotiable=False)
            .add_objective("Handle 10K users", priority=Priority.MUST_HAVE, measurable=True)
            .set_phase(CognitivePhase.DECISION, confidence=85)
            .add_reasoning_pattern(ReasoningPattern.COMPARATIVE)
            .add_reasoning_pattern(ReasoningPattern.COST_BENEFIT)
            .add_assumption("Traffic won't exceed 10K in 2 years", validated=True, confidence=75)
            .add_tension("Horizontal scaling is complex", impact=Impact.MEDIUM, mitigation="Use read replicas")
            .synthesize(
                decision="Adopt PostgreSQL 15 on AWS RDS",
                rationale="Best balance of compliance, cost, and familiarity",
            )
            .add_alternative(
                decision="Use MongoDB Atlas",
                rationale_against="Lacks ACID across collections",
            )
        )

        assert doc.decision.title == "Use PostgreSQL"
        assert doc.decision.domain == "architecture"
        assert len(doc.context.constraints) == 1
        assert doc.context.constraints[0].description == "Must support ACID"
        assert len(doc.context.objectives) == 1
        assert doc.cognitive_state.confidence == 85
        assert doc.reasoning.patterns_applied == [ReasoningPattern.COMPARATIVE, ReasoningPattern.COST_BENEFIT]
        assert len(doc.assumptions) == 1
        assert len(doc.unresolved_tensions) == 1
        assert doc.synthesis.decision == "Adopt PostgreSQL 15 on AWS RDS"
        assert len(doc.synthesis.alternatives) == 1

    def test_yaml_serialization(self):
        """Test YAML serialization roundtrip."""
        original = DecisionDocument.create(
            title="Test YAML",
            intent="Test serialization",
        ).synthesize(
            decision="It works",
            rationale="Because we tested it",
        )

        yaml_str = original.to_yaml()
        assert "drf_version:" in yaml_str
        assert "Test YAML" in yaml_str

        restored = DecisionDocument.from_yaml(yaml_str)
        assert restored.decision.title == original.decision.title
        assert restored.synthesis.decision == original.synthesis.decision

    def test_json_serialization(self):
        """Test JSON serialization roundtrip."""
        original = DecisionDocument.create(
            title="Test JSON",
            intent="Test serialization",
        ).synthesize(
            decision="It works",
            rationale="Because we tested it",
        )

        json_str = original.to_json()
        assert '"drf_version":' in json_str
        assert '"Test JSON"' in json_str

        restored = DecisionDocument.from_json(json_str)
        assert restored.decision.title == original.decision.title
        assert restored.synthesis.decision == original.synthesis.decision

    def test_file_save_and_load(self):
        """Test saving and loading from files."""
        original = DecisionDocument.create(
            title="Test File",
            intent="Test file ops",
        ).synthesize(
            decision="Files work",
            rationale="We saved and loaded",
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            # Test YAML
            yaml_path = Path(tmpdir) / "decision.yaml"
            original.save(yaml_path)
            assert yaml_path.exists()

            loaded_yaml = DecisionDocument.load(yaml_path)
            assert loaded_yaml.decision.title == original.decision.title

            # Test JSON
            json_path = Path(tmpdir) / "decision.json"
            original.save(json_path)
            assert json_path.exists()

            loaded_json = DecisionDocument.load(json_path)
            assert loaded_json.decision.title == original.decision.title

    def test_approve_decision(self):
        """Test approving a decision."""
        doc = DecisionDocument.create(
            title="Test Approval",
            intent="Test approval flow",
        ).synthesize(
            decision="Approved decision",
            rationale="It's good",
        ).approve("Alice Chen")

        assert doc.meta.status == DecisionStatus.APPROVED
        assert len(doc.meta.actors) == 1
        assert doc.meta.actors[0].name == "Alice Chen"
        assert doc.meta.actors[0].role.value == "approver"

    def test_uuid_generation(self):
        """Test that UUIDs are auto-generated."""
        doc = DecisionDocument.create(
            title="Test UUID",
            intent="Test UUID generation",
        )

        assert doc.decision.id is not None
        assert len(str(doc.decision.id)) == 36  # UUID format
