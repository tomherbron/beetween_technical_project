from flask import jsonify

from api import db
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError


class JobOffer(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    contact_name = db.Column(db.String(255))
    full_address = db.Column(db.String(255))
    city = db.Column(db.String(50))
    zip_code = db.Column(db.String(5))
    application_url = db.Column(db.String(500))
    company_name = db.Column(db.String(255))
    company_description = db.Column(db.Text())
    description = db.Column(db.Text())
    creation_date = db.Column(db.DateTime(timezone=True), default=func.now())
    contract_type = db.Column(db.String(50))
    contract_description = db.Column(db.String(255))
    duration = db.Column(db.String(100))
    id_pe = db.Column(db.String(100))

    def __init__(self, title, contact_name, full_address, city, zip_code, application_url,
                 company_name, company_description, description, creation_date, contract_type, contract_description,
                 duration, id_pe):
        self.title = title
        self.contact_name = contact_name
        self.full_address = full_address
        self.city = city
        self.zip_code = zip_code
        self.application_url = application_url
        self.company_name = company_name
        self.company_description = company_description
        self.description = description
        self.creation_date = creation_date
        self.contract_type = contract_type
        self.contract_description = contract_description
        self.duration = duration
        self.id_pe = id_pe

    @classmethod
    def get_all_job_offers(cls):

        # Retrieves all offers from DB

        try:
            job_offers = JobOffer.query.all()
            return job_offers
        except SQLAlchemyError as e:
            print(f"Error retrieving job offer: {str(e)}")

    @classmethod
    def insert_job_offer(cls, job_offer):

        # Inserts job offers into DB

        try:

            # Check if a job offer with the same id_pe already exists in the database
            existing_job_offer = JobOffer.query.filter_by(id_pe=job_offer.id_pe).first()

            if existing_job_offer:
                print("Job offer already exists in the database")
            else:
                db.session.add(job_offer)
                db.session.commit()
                print("Job offer added!")

        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error inserting job offer: {str(e)}")







