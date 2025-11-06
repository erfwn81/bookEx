from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("postbook", views.postbook, name="postbook"),
    path("displaybooks", views.displaybooks, name="displaybooks"),
    path("book_detail/<int:book_id>", views.book_detail, name="book_detail"),
    path("mybooks", views.mybooks, name="mybooks"),
    path("book_delete/<int:book_id>", views.book_delete, name="book_delete"),

    # About
    path("aboutus", views.aboutus, name="aboutus"),

    # Search
    path("search", views.search, name="search"),

    # Shopping Cart
    path("cart", views.cart_view, name="cart"),
    path("cart/add/<int:book_id>", views.cart_add, name="cart_add"),
    path("cart/remove/<int:book_id>", views.cart_remove, name="cart_remove"),
    path("cart/clear", views.cart_clear, name="cart_clear"),

    # Comments (NEW)
    path("comment/add/<int:book_id>", views.add_comment, name="add_comment"),
    path("comment/delete/<int:comment_id>", views.delete_comment, name="delete_comment"),

    # Ratings (NEW)
    path("rate/<int:book_id>", views.rate_book, name="rate_book"),

    # Favorites (NEW)
    path("favorite/toggle/<int:book_id>", views.favorite_toggle, name="favorite_toggle"),
    path("favorites", views.favorites_list, name="favorites_list"),
]
