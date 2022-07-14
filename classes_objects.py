""" Example of classes and objects """


class Pizza:
    """Models the idea of a Pizza"""

    # Attributes Definitions
    size: str
    toppings: int
    extra_cheese: bool = False

    def __init__(self, size: str, toppings: int) -> None:
        """Constructor definition"""
        """Initialize the attributes"""
        self.size = size
        self.toppings = toppings
        # self.extra_cheese = extra_cheese

    def price(self, tax: float) -> float:
        """Calculate the price of a Pizza"""
        total: float = 0.0
        # TODO --- compute price
        if self.size == "large":
            total += 10.0
        elif self.size == "medium":
            total += 8.0
        elif self.size == "small":
            total += 6.0
        else:
            raise ValueError("Invalid size")
        if self.extra_cheese:
            total += 1.0

        total *= tax

        return total


"""
def price(pizza: Pizza) -> float:
        ''' Calculate the price of a Pizza'''
        total: float = 0.0
        # TODO --- compute price
        if pizza.size == 'large':
            total += 10.0
        elif pizza.size == 'medium':
            total += 8.0
        elif pizza.size == 'small':
            total += 6.0
        else:
            raise ValueError('Invalid size')
        if pizza.extra_cheese:
            total += 1.0
        return total
"""

# Make a new Pizza
a_pizza: Pizza = Pizza("large", 2)
# a_pizza.size = 'large'
# a_pizza.toppings = 3
# a_pizza.extra_cheese = False

print(Pizza)
print(a_pizza)
print(a_pizza.size)
# Method call
print(f"Price of a Pizza: $ {a_pizza.price(1.05)}")

another_pizza: Pizza = Pizza("small", 1)
another_pizza.extra_cheese = True
print(another_pizza.size)
print(f"Price of a Pizza: $ {another_pizza.price(1.05)}")
