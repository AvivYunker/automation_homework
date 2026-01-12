'''
The "__init__.py" file tells Python that
the folder is a package (a collection of
Python modules).

We need this file because without it - Python
won't recognize the folder as a package.

'''

from .base_page import BasePage
from .login_page import LoginPage
from .search_page import SearchPage
from .product_page import ProductPage
from .cart_page import CartPage

__all__ = [
    'BasePage',
    'LoginPage',
    'SearchPage',
    'ProductPage',
    'CartPage'
]
