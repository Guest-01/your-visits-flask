from flask import Blueprint, render_template, request, current_app
from your_visits.models import db, User, Ip

bp = Blueprint("main", __name__)


@bp.route("/")
def home():
    client = {
        "remote_addr": request.remote_addr,
        "user_agent": request.headers.get("User-Agent"),
    }
    ip = Ip.query.filter_by(ip=client["remote_addr"]).first()
    if ip is None:
        current_app.logger.info(f'New IP {client["remote_addr"]}')
        ip = Ip(ip=client["remote_addr"], count=1)
        db.session.add(ip)
    else:
        ip.count += 1
    db.session.commit()
    return render_template("home.html", client=client, count=ip.count)
