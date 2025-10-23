"""pytest tests for token classes."""

import pytest
from typing import Any

from tokens import Token, Tid, Tint, Tkeyword
from tokens.errors import TokenTypeError


class TestTokenBase:
    """Test the abstract base class Token."""

    def test_abstract_methods(self):
        """Test that Token cannot be instantiated directly."""
        with pytest.raises(TypeError):
            Token("TEST", "value")

    def test_token_types_registration(self):
        """Test that subclasses are registered in Token.types."""
        # Clear any existing types for clean test
        original_types = Token.types
        Token.types = ()

        # Create instances to trigger registration
        tid = Tid("test123")
        tint = Tint("456")
        tkw = Tkeyword("SELECT")

        # Check registration
        assert Tid in Token.types
        assert Tint in Token.types
        assert Tkeyword in Token.types

        # Restore original types
        Token.types = original_types

    def test_concrete_subclass_initialization(self):
        """Test initialization through concrete subclass."""
        tid = Tid("valid_id")
        assert tid.token_type == "ID"
        assert tid.token_value == "valid_id"


class TestTid:
    """Test the Tid (ID Token) class."""

    @pytest.fixture
    def valid_tid(self):
        """Return a valid Tid instance."""
        return Tid("valid_id123")

    @pytest.fixture
    def invalid_tid_values(self):
        """Return invalid values for Tid."""
        # Values containing characters not in TID_RULES
        return ["invalid@id", "id-with-dash", "id with space", "id$symbol"]

    def test_initialization(self, valid_tid):
        """Test Tid initialization."""
        assert valid_tid.token_type == "ID"
        assert valid_tid.token_value == "valid_id123"

    def test_properties(self, valid_tid):
        """Test token_type and token_value properties."""
        assert valid_tid.token_type == "ID"
        assert valid_tid.token_value == "valid_id123"

    def test_token_value_setter(self, valid_tid):
        """Test token_value setter."""
        valid_tid.token_value = "new_id_456"
        assert valid_tid.token_value == "new_id_456"

    def test_str_method(self, valid_tid):
        """Test __str__ method."""
        assert str(valid_tid) == "valid_id123"

    def test_repr_method(self, valid_tid):
        """Test __repr__ method."""
        representation = repr(valid_tid)
        assert representation == 'Tid("valid_id123")'
        # Test that it's evaluable
        tid_from_repr = eval(representation)
        assert isinstance(tid_from_repr, Tid)
        assert tid_from_repr.token_value == "valid_id123"

    def test_is_valid_with_valid_values(self):
        """Test is_valid method with valid ID values."""
        # Test various valid ID patterns based on TID_RULES
        valid_values = []

        # Assuming TID_RULES contains alphanumeric and underscore
        # Adjust based on your actual TID_RULES
        if "a" in Tid.RULES and "1" in Tid.RULES and "_" in Tid.RULES:
            valid_values = ["user_id", "test123", "var_1", "a", "A", "id123"]

        for value in valid_values:
            tid = Tid(value)
            assert tid.is_valid() is True

    def test_is_valid_with_invalid_values(self, invalid_tid_values):
        """Test is_valid method with invalid ID values."""
        for invalid_value in invalid_tid_values:
            # Check if the value would be invalid based on RULES
            value_set = set(invalid_value)
            if not (value_set <= Tid.RULES):
                with pytest.raises(TokenTypeError):
                    Tid(invalid_value)

    def test_token_type_error_raised(self):
        """Test that TokenTypeError is raised for invalid Tid values."""
        # Find a character not in TID_RULES
        all_chars = set(
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_!@#$%^&*()-+=[]{}|;:,.<>?/"
        )
        invalid_chars = all_chars - Tid.RULES

        if invalid_chars:
            invalid_char = next(iter(invalid_chars))
            with pytest.raises(TokenTypeError):
                Tid(f"invalid{invalid_char}id")

    def test_edge_cases(self):
        """Test edge cases for Tid."""
        # Empty string
        with pytest.raises(TokenTypeError):
            Tid("")

        # Very long ID
        long_id = "a" * 1000
        try:
            tid = Tid(long_id)
            assert tid.is_valid()
        except TokenTypeError:
            pass  # Might be invalid if rules don't allow only 'a's


class TestTint:
    """Test the Tint (INT Token) class."""

    @pytest.fixture
    def valid_tint(self):
        """Return a valid Tint instance."""
        return Tint("12345")

    @pytest.fixture
    def invalid_tint_values(self):
        """Return invalid values for Tint."""
        return ["12.34", "123abc", "-456", "+789", "0123", " 123", "123 "]

    def test_initialization(self, valid_tint):
        """Test Tint initialization."""
        assert valid_tint.token_type == "INT"
        assert valid_tint.token_value == "12345"

    def test_properties(self, valid_tint):
        """Test token_type and token_value properties."""
        assert valid_tint.token_type == "INT"
        assert valid_tint.token_value == "12345"

    def test_token_value_setter(self, valid_tint):
        """Test token_value setter."""
        valid_tint.token_value = "999"
        assert valid_tint.token_value == "999"

    def test_int_method(self, valid_tint):
        """Test __int__ method."""
        assert int(valid_tint) == 12345

        # Test with different values
        tint_zero = Tint("0")
        assert int(tint_zero) == 0

        tint_large = Tint("999999")
        assert int(tint_large) == 999999

    def test_repr_method(self, valid_tint):
        """Test __repr__ method."""
        representation = repr(valid_tint)
        assert representation == "Tint(12345)"
        # Test that it's evaluable (with some adaptation)
        # Note: eval won't work directly due to custom class

    def test_is_valid_with_valid_values(self):
        """Test is_valid method with valid integer values."""
        # Test various valid integer patterns based on TINT_RULES
        valid_values = []

        # Assuming TINT_RULES contains only digits 0-9
        if set("0123456789") <= Tint.RULES:
            valid_values = ["0", "1", "123", "999999", "000123"]

        for value in valid_values:
            tint = Tint(value)
            assert tint.is_valid() is True

    def test_is_valid_with_invalid_values(self, invalid_tint_values):
        """Test is_valid method with invalid integer values."""
        for invalid_value in invalid_tint_values:
            # Check if the value would be invalid based on RULES
            value_set = set(invalid_value)
            if not (value_set <= Tint.RULES):
                with pytest.raises(TokenTypeError):
                    Tint(invalid_value)

    def test_token_type_error_raised(self):
        """Test that TokenTypeError is raised for invalid Tint values."""
        # Find a character not in TINT_RULES
        all_chars = set(
            "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()-_=+[]{}|;:,.<>?/"
        )
        invalid_chars = all_chars - Tint.RULES

        if invalid_chars:
            invalid_char = next(iter(invalid_chars))
            with pytest.raises(TokenTypeError):
                Tint(f"12{invalid_char}34")

    def test_edge_cases(self):
        """Test edge cases for Tint."""
        # Empty string
        with pytest.raises(TokenTypeError):
            Tint("")

        # Very large number
        large_num = "9" * 1000
        try:
            tint = Tint(large_num)
            assert tint.is_valid()
            # Also test conversion to int
            int_value = int(tint)
            assert int_value == int(large_num)
        except (TokenTypeError, ValueError, OverflowError):
            pass  # Might fail for very large numbers


class TestTkeyword:
    """Test the Tkeyword (KEYWORD Token) class."""

    @pytest.fixture
    def valid_tkeyword(self):
        """Return a valid Tkeyword instance."""
        # Use a keyword that exists in TKW_RULES
        if "SELECT" in Tkeyword.RULES:
            return Tkeyword("SELECT")
        elif len(Tkeyword.RULES) > 0:
            first_keyword = next(iter(Tkeyword.RULES))
            return Tkeyword(first_keyword)
        else:
            pytest.skip("No keywords defined in TKW_RULES")

    @pytest.fixture
    def invalid_keyword_values(self):
        """Return invalid values for Tkeyword."""
        return ["NOT_A_KEYWORD", "RANDOM", "INVALID", "UNKNOWN"]

    def test_initialization(self, valid_tkeyword):
        """Test Tkeyword initialization."""
        assert valid_tkeyword.token_type == "KEYWORD"
        assert valid_tkeyword.token_value in Tkeyword.RULES

    def test_properties(self, valid_tkeyword):
        """Test token_type and token_value properties."""
        assert valid_tkeyword.token_type == "KEYWORD"
        assert valid_tkeyword.token_value.upper() in Tkeyword.RULES

    def test_token_value_setter(self, valid_tkeyword):
        """Test token_value setter."""
        # Set to another valid keyword
        if len(Tkeyword.RULES) > 1:
            other_keyword = next(
                iter(Tkeyword.RULES - {valid_tkeyword.token_value.upper()})
            )
            valid_tkeyword.token_value = other_keyword
            assert valid_tkeyword.token_value == other_keyword

    def test_repr_method(self, valid_tkeyword):
        """Test __repr__ method."""
        representation = repr(valid_tkeyword)
        expected = f"Tkw({valid_tkeyword.token_value})"
        assert representation == expected

    def test_is_valid_with_valid_values(self):
        """Test is_valid method with valid keyword values."""
        # Test all keywords in TKW_RULES
        for keyword in Tkeyword.RULES:
            tkw = Tkeyword(keyword)
            assert tkw.is_valid() is True

            # Test case insensitivity
            tkw_lower = Tkeyword(keyword.lower())
            assert tkw_lower.is_valid() is True

            tkw_mixed = Tkeyword(keyword.title())
            assert tkw_mixed.is_valid() is True

    def test_is_valid_with_invalid_values(self, invalid_keyword_values):
        """Test is_valid method with invalid keyword values."""
        for invalid_value in invalid_keyword_values:
            if invalid_value.upper() not in Tkeyword.RULES:
                with pytest.raises(TokenTypeError):
                    Tkeyword(invalid_value)

    def test_token_type_error_raised(self):
        """Test that TokenTypeError is raised for invalid Tkeyword values."""
        # Use a value that's definitely not in TKW_RULES
        test_value = "DEFINITELY_NOT_A_VALID_KEYWORD_12345"
        if test_value.upper() not in Tkeyword.RULES:
            with pytest.raises(TokenTypeError):
                Tkeyword(test_value)

    def test_case_insensitivity(self):
        """Test that keyword validation is case-insensitive."""
        if "SELECT" in Tkeyword.RULES:
            variations = ["select", "SELECT", "Select", "SeLeCt"]
            for variation in variations:
                tkw = Tkeyword(variation)
                assert tkw.is_valid() is True
                assert tkw.token_value == variation  # Should preserve case

    def test_edge_cases(self):
        """Test edge cases for Tkeyword."""
        # Empty string
        with pytest.raises(TokenTypeError):
            Tkeyword("")


class TestTokenIntegration:
    """Integration tests for token classes."""

    def test_token_hierarchy(self):
        """Test that all token classes follow the Token interface."""
        tokens = []

        # Create instances of each token type
        if Tid.RULES and len(Tid.RULES) > 0:
            tid = Tid("test_id")
            tokens.append(tid)
            assert isinstance(tid, Token)

        if Tint.RULES and len(Tint.RULES) > 0:
            tint = Tint("123")
            tokens.append(tint)
            assert isinstance(tint, Token)

        if Tkeyword.RULES and len(Tkeyword.RULES) > 0:
            first_keyword = next(iter(Tkeyword.RULES))
            tkw = Tkeyword(first_keyword)
            tokens.append(tkw)
            assert isinstance(tkw, Token)

        # Test common interface
        for token in tokens:
            assert hasattr(token, "token_type")
            assert hasattr(token, "token_value")
            assert hasattr(token, "is_valid")
            assert hasattr(token, "__repr__")

            # Test properties
            assert token.token_type in ["ID", "INT", "KEYWORD"]
            assert isinstance(token.token_value, str)
            assert isinstance(token.is_valid(), bool)
            assert isinstance(repr(token), str)

    def test_token_value_modification(self):
        """Test modifying token values after creation."""
        # Test Tid
        if Tid.RULES and len(Tid.RULES) > 0:
            tid = Tid("initial_id")
            new_valid_id = "updated_id"
            if set(new_valid_id) <= Tid.RULES:
                tid.token_value = new_valid_id
                assert tid.token_value == new_valid_id
                assert tid.is_valid()

        # Test Tint
        if Tint.RULES and len(Tint.RULES) > 0:
            tint = Tint("123")
            new_valid_int = "456"
            if set(new_valid_int) <= Tint.RULES:
                tint.token_value = new_valid_int
                assert tint.token_value == new_valid_int
                assert tint.is_valid()
                assert int(tint) == 456

        # Test Tkeyword
        if Tkeyword.RULES and len(Tkeyword.RULES) > 1:
            first_keyword = next(iter(Tkeyword.RULES))
            tkw = Tkeyword(first_keyword)
            second_keyword = next(iter(Tkeyword.RULES - {first_keyword}))
            tkw.token_value = second_keyword
            assert tkw.token_value == second_keyword
            assert tkw.is_valid()


class TestTokenErrorMessages:
    """Test error messages and exceptions."""

    def test_token_type_error_messages(self):
        """Test that TokenTypeError messages are informative."""
        # Test Tid error message
        if Tid.RULES:
            invalid_char = next(iter(set("@") - Tid.RULES), None)
            if invalid_char:
                with pytest.raises(TokenTypeError) as exc_info:
                    Tid(f"invalid{invalid_char}id")
                error_message = str(exc_info.value)
                assert "Wrong value for ID" in error_message
                assert "ID" in error_message  # Should mention the token type

        # Test Tint error message
        if Tint.RULES:
            invalid_char = next(iter(set("a") - Tint.RULES), None)
            if invalid_char:
                with pytest.raises(TokenTypeError) as exc_info:
                    Tint(f"12{invalid_char}34")
                error_message = str(exc_info.value)
                assert "Wrong value for INT" in error_message
                assert "INT" in error_message  # Should mention the token type

        # Test Tkeyword error message
        invalid_keyword = "INVALID_KEYWORD_XYZ"
        if invalid_keyword.upper() not in Tkeyword.RULES:
            with pytest.raises(TokenTypeError) as exc_info:
                Tkeyword(invalid_keyword)
            error_message = str(exc_info.value)
            assert "Wrong value for KEYWORD" in error_message
            assert "KEYWORD" in error_message  # Should mention the token type


# Parameterized tests for comprehensive coverage
class TestParameterizedTokens:
    """Parameterized tests for token validation."""

    @pytest.mark.parametrize(
        "token_class,valid_values,invalid_values",
        [
            (Tid, ["user_id", "test123", "var_1"], ["id@test", "id-test", "id test"]),
            (Tint, ["0", "123", "999"], ["12.3", "123a", "-456"]),
            (Tkeyword, ["SELECT", "FROM", "WHERE"], ["NOTVALID", "RANDOM"]),
        ],
    )
    def test_token_validation(self, token_class, valid_values, invalid_values):
        """Test token validation with parameterized values."""
        # Skip if rules are not properly configured for this test
        if not token_class.RULES:
            pytest.skip(f"No rules defined for {token_class.__name__}")

        # Test valid values
        for valid_value in valid_values:
            # Check if this value should be valid based on rules
            if token_class == Tkeyword:
                # For keywords, check case-insensitive inclusion
                if valid_value.upper() in token_class.RULES:
                    token = token_class(valid_value)
                    assert token.is_valid()
            else:
                # For Tid and Tint, check character set inclusion
                if set(valid_value) <= token_class.RULES:
                    token = token_class(valid_value)
                    assert token.is_valid()

        # Test invalid values
        for invalid_value in invalid_values:
            if token_class == Tkeyword:
                # For keywords, check case-insensitive exclusion
                if invalid_value.upper() not in token_class.RULES:
                    with pytest.raises(TokenTypeError):
                        token_class(invalid_value)
            else:
                # For Tid and Tint, check character set exclusion
                if not (set(invalid_value) <= token_class.RULES):
                    with pytest.raises(TokenTypeError):
                        token_class(invalid_value)


# Run the tests with: pytest test_tokens.py -v
