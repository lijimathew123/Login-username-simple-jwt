
import pymongo

url = 'mongodb://localhost:27017'

client = pymongo.MongoClient(url)
db = client['CRM']
person_collection = db['Last_login']
default_lead_field = db['Default Lead Field']
leads_collection = db['Leads']
customer_collection = db['Customer']
company_collection = db['Company']
deal_collection = db['Deals']
default_customer_field = db['Default Customer Field']
default_company_field = db['Default Company Field']
default_deal_field = db['Default Deal Field']
default_deal_status_field = db['Default Deal Status Field']
