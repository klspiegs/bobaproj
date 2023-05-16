from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user

from ..forms import BobaReview, SearchForm, FriendSearchForm
from ..models import User, Review, BobaList, add_store
from ..utils import current_time

boba = Blueprint("boba", __name__)


""" ************ View functions ************ """


@boba.route("/", methods=["GET", "POST"])
def index():
    form = SearchForm()
    form2 = FriendSearchForm()
    return render_template("index.html", form=form, form2=form2)

@boba.route('/search', methods=['POST'])
def bsearch():
    search_form = SearchForm()
    friend_form = FriendSearchForm()

    if search_form.validate_on_submit():
        return redirect(url_for("boba.query_results", query=search_form.search_query.data))
    return render_template('index.html', form = search_form , form2=friend_form)


@boba.route('/friend_search', methods=['POST'])
def fsearch():
    search_form = SearchForm()
    friend_form = FriendSearchForm()

    if friend_form.validate_on_submit():
        return redirect(url_for("boba.query_friend_results", query=friend_form.friend_search_query.data))
    return render_template('index.html', form = search_form , form2=friend_form)


@boba.route("/search-results/<query>", methods=["GET"])
def query_results(query):
    add_store(query, "1399 New York Ave NW, Washington, DC 20005")
    results = BobaList.objects(name=query)
    return render_template("query.html", results=results, )

@boba.route("/search-friend-results/<query>", methods=["GET"])
def query_friend_results(query):
    results = User.objects(username=query)
    return render_template("friendquery.html", results=results)


@boba.route("/boba/<boba_id>", methods=["GET", "POST"])
def boba_detail(boba_id):

    result = BobaList.objects.get(boba_id=boba_id)
    form = BobaReview()
    if form.validate_on_submit() and current_user.is_authenticated:
        review = Review(
            commenter=current_user._get_current_object(),
            content=form.text.data,
            date=current_time(),
            boba_name=result.name,
            boba_id = result.boba_id,
        )
        review.save()
        current_user._get_current_object().modify(points= current_user._get_current_object().points + 50)
        current_user._get_current_object().save()
        return redirect(request.path)

    reviews = Review.objects(boba_id=boba_id)
    print(result.name)
    return render_template(
        "boba_detail.html", form=form, boba=result, reviews=reviews
    )


@boba.route("/user/<username>")
def user_detail(username):
    user = User.objects(username=username).first()
    reviews = Review.objects(commenter=user)

    return render_template("user_detail.html", username=username, reviews=reviews)

@boba.route("/about")
def about():
    return render_template("about.html")