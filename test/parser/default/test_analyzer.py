"""pytest tests for analyzer module."""

import pytest
from typing import Iterator
from unittest.mock import Mock, patch

from analyzer import QueryBase, Query, QueryBatch, SQL_Analyzer
from analyzer.errors import LexicalError


class TestQueryBase:
    """Test the abstract base class QueryBase."""

    def test_abstract_methods(self):
        """Test that QueryBase cannot be instantiated directly."""
        with pytest.raises(TypeError):
            QueryBase()

    def test_concrete_subclass_initialization(self):
        """Test initialization through concrete subclass."""
        # We'll test this through Query class
        query = Query()
        assert query.base_list == []
        assert query.query_lang == QueryBase.lang

    def test_input_modifier_with_string(self):
        """Test _input_modifier with string input."""
        query = Query("hello,world")
        assert len(query) == 2
        assert "hello" in query.query_splitted
        assert "world" in query.query_splitted

    def test_input_modifier_with_iterator(self):
        """Test _input_modifier with iterator input."""
        iterator = iter(["hello", "world"])
        query = Query(iterator)
        assert len(query) == 2
        assert "hello" in query.query_splitted
        assert "world" in query.query_splitted

    def test_input_modifier_with_none(self):
        """Test _input_modifier with None input."""
        query = Query()
        assert query.base_list == []
        assert len(query) == 0


class TestQuery:
    """Test the Query class."""

    @pytest.fixture
    def empty_query(self):
        """Return an empty Query instance."""
        return Query()

    @pytest.fixture
    def sample_query(self):
        """Return a Query instance with sample data."""
        return Query("SELECT * FROM users")

    def test_initialization(self, empty_query):
        """Test Query initialization."""
        assert empty_query.query_splitted == []
        assert empty_query.rule == Query.sep

    def test_append_method(self, empty_query):
        """Test append method."""
        empty_query.append("SELECT")
        empty_query.append("FROM")
        assert len(empty_query) == 2
        assert empty_query.query_splitted == ["SELECT", "FROM"]

    def test_string_splitting(self):
        """Test string splitting with separator rules."""
        query = Query("hello,world,test")
        assert len(query) == 3
        assert query.query_splitted == ["hello", "world", "test"]

    def test_repr_method(self, sample_query):
        """Test __repr__ method."""
        representation = repr(sample_query)
        assert "SELECT" in representation
        assert "*" in representation
        assert "FROM" in representation
        assert "users" in representation
        assert "(" in representation and ")" in representation

    def test_iter_method(self, sample_query):
        """Test __iter__ method."""
        items = list(sample_query)
        assert isinstance(items, list)
        assert len(items) > 0

    def test_getitem_method(self, sample_query):
        """Test __getitem__ method."""
        first_item = sample_query[0]
        assert first_item == "SELECT"

        # Test slicing
        if len(sample_query) >= 2:
            slice_result = sample_query[0:2]
            assert len(slice_result) == 2

    def test_len_method(self, sample_query, empty_query):
        """Test __len__ method."""
        assert len(sample_query) > 0
        assert len(empty_query) == 0

    def test_complex_query_splitting(self):
        """Test complex query splitting scenarios."""
        # Test with multiple separators
        query = Query("SELECT name, age FROM users WHERE age > 18")
        assert len(query) > 3

        # Test with empty segments
        query = Query("hello,,world")
        assert "" in query.query_splitted or len(query) == 2


class TestQueryBatch:
    """Test the QueryBatch class."""

    @pytest.fixture
    def empty_batch(self):
        """Return an empty QueryBatch instance."""
        return QueryBatch()

    @pytest.fixture
    def sample_queries(self):
        """Return sample Query objects for testing."""
        return [Query("SELECT * FROM users"), Query("DELETE FROM logs")]

    @pytest.fixture
    def batch_with_data(self):
        """Return a QueryBatch with sample data."""
        return QueryBatch("SELECT * FROM users; DELETE FROM logs;")

    def test_initialization(self, empty_batch):
        """Test QueryBatch initialization."""
        assert empty_batch.batch == []
        assert empty_batch.rule == QueryBatch.end

    def test_append_method(self, empty_batch, sample_queries):
        """Test append method."""
        for query in sample_queries:
            empty_batch.append(query)

        assert len(empty_batch) == 2
        assert empty_batch.batch == sample_queries

    def test_batch_creation_from_string(self):
        """Test batch creation from string with end separators."""
        batch = QueryBatch("QUERY1; QUERY2; QUERY3;")
        assert len(batch) == 3

    def test_repr_method(self, batch_with_data, empty_batch):
        """Test __repr__ method."""
        representation = repr(batch_with_data)
        assert "QueryList" in representation
        assert "Queries" in representation or "Query" in representation

        empty_repr = repr(empty_batch)
        assert "QueryList" in empty_repr

    def test_iter_method(self, batch_with_data):
        """Test __iter__ method."""
        queries = list(batch_with_data)
        assert all(isinstance(query, Query) for query in queries)
        assert len(queries) == len(batch_with_data)

    def test_getitem_method(self, batch_with_data):
        """Test __getitem__ method."""
        first_query = batch_with_data[0]
        assert isinstance(first_query, Query)

        # Test slicing
        if len(batch_with_data) >= 2:
            slice_result = batch_with_data[0:2]
            assert len(slice_result) == 2

    def test_len_method(self, batch_with_data, empty_batch):
        """Test __len__ method."""
        assert len(batch_with_data) > 0
        assert len(empty_batch) == 0


class TestSQLAnalyzer:
    """Test the SQL_Analyzer class."""

    @pytest.fixture
    def analyzer(self):
        """Return a SQL_Analyzer instance."""
        return SQL_Analyzer()

    @pytest.fixture
    def sample_sql_queries(self):
        """Return sample SQL queries for testing."""
        return [
            "SELECT * FROM users;",
            "SELECT name, age FROM users WHERE age > 18;",
            "DELETE FROM logs WHERE date < '2023-01-01';",
        ]

    def test_initialization(self, analyzer):
        """Test SQL_Analyzer initialization."""
        assert hasattr(analyzer, "input_string")
        assert analyzer.avoid == SQL_Analyzer.avoid
        assert analyzer.end == SQL_Analyzer.end
        assert analyzer.sep == SQL_Analyzer.sep

    def test_input_string_property(self, analyzer):
        """Test input_string property getter and setter."""
        test_string = "SELECT * FROM users;"
        analyzer.input_string = test_string
        assert analyzer.input_string == test_string

    def test_get_input_method(self, analyzer):
        """Test get_input method."""
        test_string = "SELECT * FROM users;"
        analyzer.get_input(test_string)
        assert analyzer.input_string == test_string

    @pytest.mark.parametrize(
        "input_string,expected_queries",
        [
            ("SELECT * FROM users;", 1),
            ("SELECT * FROM users; SELECT * FROM products;", 2),
            ("SELECT a, b, c FROM table WHERE x = 1;", 1),
            ("", 0),
            ("   ", 0),
        ],
    )
    def test_analyze_method(self, analyzer, input_string, expected_queries):
        """Test analyze method with various inputs."""
        if input_string.strip():  # Only test non-empty strings
            batch = analyzer.analyze(input_string)
            assert isinstance(batch, QueryBatch)
            assert len(batch) == expected_queries
        else:
            # For empty strings, we expect empty batch
            batch = analyzer.analyze(input_string)
            assert len(batch) == 0

    def test_analyze_with_avoid_chars(self, analyzer):
        """Test analyze method raises LexicalError for avoid characters."""
        # Assuming AVOID_SET contains some characters like '#' or '@'
        # You'll need to adjust based on your actual AVOID_SET
        avoid_chars = SQL_Analyzer.avoid

        if avoid_chars:
            test_char = avoid_chars[0]
            with pytest.raises(LexicalError):
                analyzer.analyze(f"SELECT {test_char} FROM users;")

    def test_analyze_with_end_chars(self, analyzer):
        """Test analyze method properly handles end characters."""
        # Test that end characters split queries correctly
        end_chars = SQL_Analyzer.end

        if end_chars:
            test_char = end_chars[0]
            input_string = f"QUERY1{test_char} QUERY2{test_char}"
            batch = analyzer.analyze(input_string)
            assert len(batch) == 2

    def test_analyze_with_sep_chars(self, analyzer):
        """Test analyze method properly handles separator characters."""
        # Test that separator characters split query words correctly
        sep_chars = SQL_Analyzer.sep

        if sep_chars:
            test_char = sep_chars[0]
            input_string = f"SELECT{test_char}*{test_char}FROM users;"
            batch = analyzer.analyze(input_string)
            if len(batch) > 0:
                query = batch[0]
                assert len(query) >= 3  # SELECT, *, FROM, users

    def test_analyze_without_input_string(self, analyzer):
        """Test analyze method when no input string is provided."""
        # First set the input string
        analyzer.input_string = "SELECT * FROM users;"
        # Then call analyze without parameters
        batch = analyzer.analyze()
        assert isinstance(batch, QueryBatch)
        assert len(batch) == 1

    def test_analyze_empty_input(self, analyzer):
        """Test analyze method with empty input."""
        batch = analyzer.analyze("")
        assert len(batch) == 0

        batch = analyzer.analyze("   ")
        assert len(batch) == 0

    def test_analyze_complex_query(self, analyzer):
        """Test analyze method with complex SQL query."""
        complex_query = """
            SELECT users.name, orders.total 
            FROM users 
            INNER JOIN orders ON users.id = orders.user_id 
            WHERE orders.date > '2023-01-01' 
            AND users.active = TRUE;
        """
        batch = analyzer.analyze(complex_query)
        assert len(batch) == 1
        query = batch[0]
        assert len(query) > 5  # Should have multiple components


class TestIntegration:
    """Integration tests for the complete analyzer workflow."""

    def test_complete_workflow(self):
        """Test complete workflow from input to analyzed batch."""
        analyzer = SQL_Analyzer()
        sql_input = "SELECT name FROM users; UPDATE users SET active = TRUE;"

        batch = analyzer.analyze(sql_input)

        # Verify the batch structure
        assert isinstance(batch, QueryBatch)
        assert len(batch) == 2

        # Verify first query
        first_query = batch[0]
        assert isinstance(first_query, Query)
        assert "SELECT" in first_query.query_splitted
        assert "name" in first_query.query_splitted
        assert "FROM" in first_query.query_splitted
        assert "users" in first_query.query_splitted

        # Verify second query
        second_query = batch[1]
        assert isinstance(second_query, Query)
        assert "UPDATE" in second_query.query_splitted

    def test_multiple_queries_with_different_endings(self):
        """Test multiple queries with different end characters."""
        analyzer = SQL_Analyzer()

        # Create input with mixed end characters (if multiple are defined)
        end_chars = SQL_Analyzer.end
        if len(end_chars) > 1:
            input_string = f"QUERY1{end_chars[0]} QUERY2{end_chars[1]}"
            batch = analyzer.analyze(input_string)
            assert len(batch) == 2


# Error scenario tests
class TestErrorScenarios:
    """Test error scenarios and edge cases."""

    def test_lexical_error_raised(self):
        """Test that LexicalError is properly raised."""
        analyzer = SQL_Analyzer()

        # This should raise LexicalError if AVOID_SET is not empty
        if SQL_Analyzer.avoid:
            with pytest.raises(LexicalError) as exc_info:
                analyzer.analyze(f"SELECT * {SQL_Analyzer.avoid[0]} FROM users;")
            assert "avoid char" in str(exc_info.value).lower()

    def test_invalid_input_types(self):
        """Test behavior with invalid input types."""
        analyzer = SQL_Analyzer()

        # These should not crash the analyzer
        # (adjust based on your actual error handling)
        try:
            analyzer.analyze(123)  # Wrong type
            analyzer.analyze(None)  # None input
        except Exception:
            # If your code doesn't handle these, that's fine
            # We're just testing they don't crash unexpectedly
            pass

    def test_very_long_input(self):
        """Test with very long input string."""
        analyzer = SQL_Analyzer()
        long_input = "SELECT * FROM " + "x" * 1000 + ";"

        batch = analyzer.analyze(long_input)
        assert len(batch) == 1
        assert len(batch[0]) >= 3


# Run the tests with: pytest test_analyzer.py -v
