from flask import (
    Blueprint,
    render_template,
    request,
    current_app,
    redirect,
    url_for,
    flash,
    session,
    g,
)
from werkzeug.security import check_password_hash, generate_password_hash
from your_visits.models import db, User, Ip

bp = Blueprint("main", __name__)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    current_app.logger.debug(user_id)
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


@bp.route("/")
def home():
    ip = Ip.query.filter_by(ip=request.remote_addr).first()
    if ip:
        ip.count += 1
    else:
        ip = Ip(ip=request.remote_addr, count=1)
        current_app.logger.info(f"new IP: {ip.ip}")
    if g.user:
        ip.user_id = g.user.id
    db.session.commit()

    if g.user:
        user = User.query.get(g.user.id)
        user_info = {
            "user": user,
            "ips": user.ips,
            "total_count": sum([ip.count for ip in user.ips]),
        }
    else:
        user_info = None

    return render_template("home.html", current_ip=ip, user_info=user_info)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        error = None
        user = User.query.filter_by(username=username).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif check_password_hash(user.password, password):
            error = "비밀번호가 올바르지 않습니다."
        else:
            session.clear()
            session["user_id"] = user.id
            return redirect(url_for("main.home"))
        flash(error)
    return render_template("login.html")


@bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form.get("username")).first()
        if user:
            flash("이미 존재하는 사용자입니다.")
        else:
            user = User(
                username=request.form.get("username"),
                password=generate_password_hash(request.form.get("password1")),
            )
            db.session.add(user)
            db.session.commit()
        return redirect(url_for("main.home"))
    return render_template("signup.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.home"))
