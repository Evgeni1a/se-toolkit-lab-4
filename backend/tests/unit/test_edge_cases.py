"""Unit tests for edge cases and boundary values."""

import pytest
from sqlmodel import Field

from app.models.item import ItemCreate, ItemUpdate
from app.models.learner import LearnerCreate
from app.models.interaction import InteractionLogCreate


class TestItemCreateValidation:
    """Tests for ItemCreate schema edge cases."""

    def test_item_create_with_empty_string_title(self) -> None:
        """ItemCreate should accept empty string title (boundary value)."""
        item = ItemCreate(title="")
        assert item.title == ""
        assert item.type == "step"
        assert item.parent_id is None

    def test_item_create_with_very_long_title(self) -> None:
        """ItemCreate should accept very long titles (boundary value)."""
        long_title = "a" * 10000
        item = ItemCreate(title=long_title)
        assert item.title == long_title
        assert len(item.title) == 10000

    def test_item_create_with_parent_id_zero(self) -> None:
        """ItemCreate with parent_id=0 should be valid (boundary value)."""
        item = ItemCreate(title="Test", parent_id=0)
        assert item.parent_id == 0

    def test_item_create_with_negative_parent_id(self) -> None:
        """ItemCreate with negative parent_id should be valid (edge case)."""
        item = ItemCreate(title="Test", parent_id=-1)
        assert item.parent_id == -1


class TestLearnerCreateValidation:
    """Tests for LearnerCreate schema edge cases."""

    def test_learner_create_with_empty_name(self) -> None:
        """LearnerCreate should accept empty name (boundary value)."""
        learner = LearnerCreate(name="", email="test@example.com")
        assert learner.name == ""
        assert learner.email == "test@example.com"

    def test_learner_create_with_email_missing_at_symbol(self) -> None:
        """LearnerCreate does not validate email format (edge case)."""
        learner = LearnerCreate(name="Test", email="invalid-email")
        assert learner.email == "invalid-email"

    def test_learner_create_with_very_long_name(self) -> None:
        """LearnerCreate should accept very long names (boundary value)."""
        long_name = "n" * 5000
        learner = LearnerCreate(name=long_name, email="test@example.com")
        assert learner.name == long_name
        assert len(learner.name) == 5000


class TestInteractionLogCreateValidation:
    """Tests for InteractionLogCreate schema edge cases."""

    def test_interaction_create_with_zero_learner_id(self) -> None:
        """InteractionLogCreate with learner_id=0 (boundary value)."""
        interaction = InteractionLogCreate(learner_id=0, item_id=1, kind="attempt")
        assert interaction.learner_id == 0

    def test_interaction_create_with_zero_item_id(self) -> None:
        """InteractionLogCreate with item_id=0 (boundary value)."""
        interaction = InteractionLogCreate(learner_id=1, item_id=0, kind="attempt")
        assert interaction.item_id == 0

    def test_interaction_create_with_very_long_kind(self) -> None:
        """InteractionLogCreate with very long kind (boundary value)."""
        long_kind = "k" * 1000
        interaction = InteractionLogCreate(learner_id=1, item_id=1, kind=long_kind)
        assert interaction.kind == long_kind
        assert len(interaction.kind) == 1000
