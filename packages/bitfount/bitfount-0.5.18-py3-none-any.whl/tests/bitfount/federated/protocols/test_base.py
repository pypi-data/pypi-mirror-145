"""Tests base protocols module."""
from typing import cast
from unittest.mock import Mock

import pytest

from bitfount.federated.protocols.base import _BaseProtocolFactory
from tests.utils.helper import unit_test


@unit_test
def test_load() -> None:
    """Test BaseProtocolFactory.load() works."""
    # Get unbound classmethod for ease of testing
    load_classmethod = cast(classmethod, _BaseProtocolFactory.load).__func__

    mock_serialized_protocol = Mock()

    # Test with a cls with `get_schema`
    mock_cls = Mock(spec_set=["get_schema"])
    loaded = load_classmethod(mock_cls, mock_serialized_protocol)
    assert loaded == mock_cls.get_schema.return_value.load.return_value
    mock_cls.get_schema.return_value.load.assert_called_once_with(
        mock_serialized_protocol
    )

    # Test with a cls with no `get_schema`
    with pytest.raises(
        AttributeError, match="Chosen protocol class does not implement get_schema"
    ):
        mock_cls = Mock(spec_set=[])
        load_classmethod(mock_cls, mock_serialized_protocol)
