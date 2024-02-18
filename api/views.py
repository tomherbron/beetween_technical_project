from flask import Blueprint, render_template, redirect
from api.services import JobOfferService, APICallService

views = Blueprint('views', __name__)


@views.route('/', methods=['GET'])
def index():
    job_offers = JobOfferService.get_all_job_offers_from_db()
    return render_template("home.html", job_offers=job_offers)


@views.route('/refresh', methods=['GET'])
def refresh_offers():
    APICallService.get_API_job_offers()
    return redirect('/')
