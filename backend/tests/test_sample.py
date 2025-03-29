
def test_addition():
    """Test that simple addition works correctly."""
    assert 1 + 1 == 2

def test_string_concatenation():
    """Test that string concatenation works correctly."""
    assert "Hello, " + "World!" == "Hello, World!"

def test_list_operations():
    """Test basic list operations."""
    my_list = [1, 2, 3]
    my_list.append(4)
    assert len(my_list) == 4
    assert my_list == [1, 2, 3, 4]
