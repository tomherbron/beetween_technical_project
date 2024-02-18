from datetime import datetime
import requests
from flask import make_response, json
from api.models import JobOffer


class JobOfferService:

    @classmethod
    def insert_job_offers(cls, job_offer_data):

        # Accessing nested keys, iterate over each job offer and assign each value to my object attributes

        for offer_data in job_offer_data['peJobs']['results']:

            title = offer_data['title']

            contact_name = None
            if offer_data['contact']:
                contact_name = offer_data['contact']['name']

            full_address = offer_data['place']['fullAddress']
            city = offer_data['place']['city']
            zip_code = offer_data['place']['zipCode']
            application_url = offer_data['url']
            company_name = offer_data['company']['name']

            company_description = None
            if 'description' in offer_data['company']:
                company_description = offer_data['company'].get('description')

            description = offer_data['job']['description']

            creation_date_str = offer_data['job']['creationDate'][:-1]
            creation_date = datetime.strptime(creation_date_str, "%Y-%m-%dT%H:%M:%S.%f")

            contract_type = offer_data['job']['contractType']
            contract_description = offer_data['job']['contractDescription']

            duration = None
            if 'duration' in offer_data['job']:
                duration = offer_data['job'].get('duration')

            id_pe = offer_data['job']['id']

            # Creation of a new job offer instance

            job_offer = JobOffer(title, contact_name, full_address, city, zip_code, application_url, company_name,
                                 company_description, description, creation_date, contract_type, contract_description,
                                 duration, id_pe)

            # Calling the model layer method to insert the object in db

            JobOffer.insert_job_offer(job_offer)

    @classmethod
    def get_all_job_offers_from_db(cls):
        return JobOffer.get_all_job_offers()


class APICallService:

    @classmethod
    def get_API_job_offers(cls):

        # URL and parameters for the api request

        url = "https://labonnealternance.apprentissage.beta.gouv.fr/api/v1/jobs"
        params = {
            "romes": "D1101",
            "caller": "tom.herbron@proton.me",
            "latitude": "48.083328",
            "longitude": "-1.68333",
            "radius": "50",
            "insee": "35238",
            "sources": "offres"
        }

        response = requests.get(url, params=params)

        # If the request is successful, parse response to json and call db insertion service

        if response.status_code == 200:
            job_offer_data = response.content
            job_offer_data = json.loads(job_offer_data)
            JobOfferService.insert_job_offers(job_offer_data)

            # For refresh feature, get all offers again

            job_offers = JobOfferService.get_all_job_offers_from_db()
            return job_offers

        else:
            return make_response('Error', response.status_code)

