from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q

from .models import MainMenu, Book
from .forms import BookForm


# ========= Core pages =========

def index(request):
    return render(
        request, "bookMng/index.html",
        {"item_list": MainMenu.objects.all()}
    )


def postbook(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            if request.user.is_authenticated:
                book.username = request.user
            book.save()
            if getattr(book, "picture", None):
                try:
                    book.pic_path = str(book.picture.name)
                    book.save(update_fields=["pic_path"])
                except Exception:
                    pass
            return HttpResponseRedirect("/displaybooks")
    else:
        form = BookForm()

    return render(
        request, "bookMng/postbook.html",
        {"item_list": MainMenu.objects.all(), "form": form}
    )


def displaybooks(request):
    books = Book.objects.all().order_by("name")
    return render(
        request, "bookMng/displaybooks.html",
        {"item_list": MainMenu.objects.all(), "books": books}
    )


def mybooks(request):
    if request.user.is_authenticated:
        books = Book.objects.filter(username=request.user).order_by("name")
    else:
        books = Book.objects.none()

    return render(
        request, "bookMng/mybooks.html",
        {"item_list": MainMenu.objects.all(), "books": books}
    )


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(
        request, "bookMng/book_detail.html",
        {"item_list": MainMenu.objects.all(), "book": book}
    )


def book_delete(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return render(
        request, "bookMng/book_delete.html",
        {"item_list": MainMenu.objects.all()}
    )


# ========= Registration =========

class Register(CreateView):
    template_name = "registration/register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("register-success")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["item_list"] = MainMenu.objects.all()
        ctx["next"] = self.request.GET.get("next", "")
        return ctx

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


# ========= About =========

def aboutus(request):
    return render(
        request, "bookMng/aboutus.html",
        {"item_list": MainMenu.objects.all()}
    )


# ========= Search =========

def search(request):
    q = request.GET.get("q", "").strip()
    results = Book.objects.none()
    if q:
        results = Book.objects.filter(
            Q(name__icontains=q) | Q(web__icontains=q)
        ).order_by("name")

    return render(
        request, "bookMng/search.html",
        {"item_list": MainMenu.objects.all(), "q": q, "results": results}
    )


# ========= Shopping Cart (session-based) =========

def _get_cart(request):
    """
    Cart structure stored in session as dict: { "book_id": quantity, ... }
    """
    cart = request.session.get("cart", {})
    request.session["cart"] = cart  # ensure it exists
    return cart


def cart_view(request):
    cart = _get_cart(request)
    ids = [int(k) for k in cart.keys()]
    items = Book.objects.filter(id__in=ids)

    rows = []
    total = 0.0
    for b in items:
        qty = int(cart.get(str(b.id), 0))
        line = float(b.price) * qty if b.price is not None else 0.0
        total += line
        rows.append({"book": b, "qty": qty, "line": line})

    return render(
        request, "bookMng/cart.html",
        {
            "item_list": MainMenu.objects.all(),
            "rows": rows,
            "total": total,
        }
    )


def cart_add(request, book_id):
    cart = _get_cart(request)
    cart[str(book_id)] = int(cart.get(str(book_id), 0)) + 1
    request.session.modified = True
    # go back to where user was, or to /cart
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/cart"))


def cart_remove(request, book_id):
    cart = _get_cart(request)
    cart.pop(str(book_id), None)
    request.session.modified = True
    return HttpResponseRedirect("/cart")


def cart_clear(request):
    request.session["cart"] = {}
    request.session.modified = True
    return HttpResponseRedirect("/cart")
