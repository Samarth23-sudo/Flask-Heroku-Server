from flask import Flask, jsonify
from flask import Flask, request
from pymongo import MongoClient
from datetime import datetime
from flask_cors import CORS
 
app = Flask(__name__)
CORS(app)

# MongoDB connection URI
uri = "mongodb+srv://tanaygad:192837465@dass.tqizd9y.mongodb.net/"
client = MongoClient(uri)

@app.route('/')
def start():
    return "This is our webserver"
# Define a route to handle the AJAX request
@app.route('/get-image-url')
def get_image_url():
    try:
        database = client['Initial_database']
        collection = database['items']
        document1 = collection.find_one(
            {'approved': 0, 'recommended': 0, 'type': "product"})
        document2 = collection.find_one(
            {'approved': 0, 'recommended': 0, 'type': "craft"})
        document3 = collection.find_one(
            {'approved': 0, 'recommended': 0, 'type': "blog"})
        print(document1)
        if document1:
            # Assuming the image URL is stored in a field called 'image-url'
            image_url1 = document1['image-url']
            description1 = document1['caption']
            url1 = document1['url-link']
            image_url2 = ""
            image_url3 = ""
            url2 = ""
            url3 = ""
            description2 = ""
            description3 = ""
            if (document2):
                # Assuming the image URL is stored in a field called 'image-url'
                image_url2 = document2['image-url']
                description2 = document2['caption']
                url2 = document2['url-link']
            if (document3):
                # Assuming the image URL is stored in a field called 'image-url'
                image_url3 = document3['image-url']
                description3 = document3['caption']
                url3 = document3['url-link']
            # Send the image URL as JSON
            return jsonify(image_url1=image_url1, description1=description1, url1=url1, image_url2=image_url2, description2=description2, url2=url2, image_url3=image_url3, description3=description3, url3=url3)
            # 1-product 2-craft 3-blog
        else:
            return jsonify(error='Document not found'), 404
    except Exception as e:
        return jsonify(error=str(e)), 500


@app.route('/send-edited-response', methods=['POST', 'GET'])
def receive_edited_content():
    try:
        data = request.json
        url = data['url']
        updated_data = data['updateData']

        # Process the received data as needed
        print("Received URL:", url)
        print("Updated Data:", updated_data)

        # Here you can perform further processing or return a response
        # For example, return a success message
        database = client['Initial_database']
        collection = database['items']
        document = collection.find_one({'url-link': url})
        if document:
            # Update the description
            collection.update_one(
                {'url-link': url},
                {'$set': {'caption': updated_data}}
            )

        return {'message': 'Data received successfully'}, 200
    except Exception as e:
        # Handle any exceptions that occur during processing
        print("Error:", e)
        return {'error': 'An error occurred'}, 500


@app.route('/post')
def get_post_ready():
    try:
        database = client['Initial_database']
        collection = database['items']
        today_date = datetime.today().strftime('%Y-%m-%d')
        document = collection.find_one(
            {'approved': {'$in': [1,2,3]}, 'recommended': 0, 'date_to_post': today_date})
        if document:
            # Assuming the image URL is stored in a field called 'image-url'
            image_url = document['image-url']
            description = document['caption']
            height = document['img-height']
            width = document['img-width']
            url = document['url-link']
            platform = document['approved']
            collection.update_many(
                {'url-link': url},
                {'$set': {'recommended': 1}}
            )
            # Send the image URL as JSON
            return jsonify(image_url=image_url, description=description, width=width, height=height,platform=platform)
        else:
            return jsonify(error='Document not found'), 404
    except Exception as e:
        return jsonify(error=str(e)), 500


@app.route('/send-approval', methods=['POST', 'GET'])
def receive_approval():
    try:
        data = request.json
        url = data['url']
        approval = data['approved']
        date = data['date']
        # Process the received data as needed

        # Here you can perform further processing or return a response
        # For example, return a success message
        database = client['Initial_database']
        collection = database['items']
        document = collection.find_one({'url-link': url})
        if document:
            print("Received URL:", url)
            print("approved:", approval)
            print("date:", date)
        # Update the description
        collection.update_many(
        {'url-link': url},
        {'$set': {'approved': approval, 'date_to_post': date}}
        )
        return {'message': 'Data received successfully'}, 200
    except Exception as e:
        # Handle any exceptions that occur during processing
        print("Error:", e)
        return {'error': 'An error occurred'}, 500

 
# if __name__ == '__main__':
#     app.run(debug=True)  # Run the Flask app in debug mode