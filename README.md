# drf-py

Python library for [DRF (Decision Reasoning Format)](https://github.com/reasoning-formats/reasoning-formats) and CRF (Context Reasoning Format).

## Installation

```bash
pip install drf
```

## Quick Start

### Creating a DRF Decision Document

```python
from drf import Decision, Constraint, Objective, Synthesis

# Create a decision
decision = Decision(
    title="Use PostgreSQL for Primary Database",
    domain="architecture",
    intent="Select a database that meets scalability and compliance requirements"
)

# Add context
decision.add_constraint(
    description="Must support ACID transactions",
    source="regulatory",
    negotiable=False
)
decision.add_objective(
    description="Handle 10,000 concurrent users",
    priority="must_have",
    measurable=True
)

# Set cognitive state
decision.set_phase("decision", confidence=85)

# Add synthesis
decision.synthesize(
    decision="Adopt PostgreSQL 15 on AWS RDS",
    rationale="Best balance of ACID compliance, cost, and team familiarity"
)

# Save to YAML
decision.save("decisions/database-selection.yaml")
```

### Loading and Validating

```python
from drf import Decision

# Load from file
decision = Decision.load("decisions/database-selection.yaml")

# Validate against schema
errors = decision.validate()
if errors:
    print(f"Validation errors: {errors}")
else:
    print(f"Decision: {decision.synthesis.decision}")
```

### Working with CRF Context

```python
from crf import Context, Policy, Fact

# Create organizational context
ctx = Context()

# Add a policy
ctx.add_policy(
    name="No Kubernetes Migration",
    description="Moratorium on K8s adoption until Q4 2024",
    status="active"
)

# Add a fact
ctx.add_fact(
    name="Current Database",
    fact_type="status",
    value="PostgreSQL 14"
)

# Save context graph
ctx.save("context/organization.yaml")
```

## Features

- **Pydantic Models**: Fully typed models for DRF and CRF documents
- **Validation**: Validate against official JSON Schema
- **Serialization**: Load/save YAML and JSON formats
- **Builder Pattern**: Fluent API for constructing documents
- **Type Safety**: Full mypy support

## Documentation

See the [reasoning-formats specification](https://github.com/reasoning-formats/reasoning-formats) for complete documentation.

## License

Apache 2.0
