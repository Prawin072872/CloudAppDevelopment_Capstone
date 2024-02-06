from cloudant.client import Cloudant
from cloudant.query import Query
from flask import Flask, jsonify, request
import atexit

#Add your Cloudant service credentials here
cloudant_username = 'e180e269-df92-4b84-920f-cda77fa52196-bluemix'
cloudant_api_key = 'esNNutBwLBLIqnOnI45mGN8_9gU1TntBDqQn5UUvu4Fe'
cloudant_url = 'https://e180e269-df92-4b84-920f-cda77fa52196-bluemix.cloudantnosqldb.appdomain.cloud'
client = Cloudant.iam(cloudant_username, cloudant_api_key, connect=True, url=cloudant_url)

session = client.session()
print('Databases:', client.all_dbs())

db = client['reviews']

app = Flask(__name__)

@app.route('/api/get_reviews', methods=['GET'])

def get_reviews():
    dealership_id = request.args.get('id')

    if dealership_id is None:
        return jsonify({"error": "Missing 'id' parameter in the URL"}),400
    

    try:
        dealership_id = int(dealership_id)
    except ValueError:
        return jsonify({"error": "'id' paramater must be an integer"}),400
    

    selector = {
        'dealership': dealership_id
    }

    result = db.get_query_result(selector)

    data_list = []

    for doc in result:
        data_list.append(doc)
    

    return jsonify(data_list)


@app.route('/api/post_review', methods=['POST'])

def post_review():
    if not request.json:
        abort(400, description='Invalid JSON data')

    review_data = request.json

    required_fields = ['id', 'name', 'dealership', 'review', 'purchase', 'purchase_date', 'car_make', 'car_model', 'car_year']
    for field in required_fields:
        if field not in review_data:
            abort(400, description = f'Missing required field: {field}')


    db.create_document(review_data)

    return jsonify({'message': "Review Posted Successfully"}),201

if __name__ == '__main__':
    app.run(debug=True)