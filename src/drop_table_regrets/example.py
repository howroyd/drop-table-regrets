"""Example module with a simple greeting function."""


def greet(name: str = "World") -> str:
    """
    Generate a greeting message.

    Args:
        name: The name to greet. Defaults to "World".

    Returns:
        A greeting message string.
    """
    return f"Hello, {name}!"


def add_numbers(a: int, b: int) -> int:
    """
    Add two numbers together.

    Args:
        a: The first number.
        b: The second number.

    Returns:
        The sum of a and b.
    """
    return a + b
