from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, logout_user

from ..services.auth_service import authenticate_user, login_authenticated_user
from .forms import LoginForm


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        user = authenticate_user(form.username.data, form.password.data)
        if user is None:
            flash("Invalid username or password.", "error")
        else:
            login_authenticated_user(user, remember=form.remember_me.data)
            next_url = request.args.get("next")
            return redirect(next_url or url_for("main.dashboard"))

    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("You have been signed out.", "success")
    return redirect(url_for("auth.login"))
