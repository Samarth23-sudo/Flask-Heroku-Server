from flask import Flask, jsonify
from flask import Flask, request
from pymongo import MongoClient
from datetime import datetime

 
app = Flask(__name__)
 
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
        document = collection.find_one({ 'approved' : 0 , 'recommended' : 0})
        print(document)
        if document:
            image_url = document['image-url']  # Assuming the image URL is stored in a field called 'image-url'
            description = document['caption']
            url = document['url-link']
            return jsonify(image_url=image_url,description=description,url=url)  # Send the image URL as JSON
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
        document = collection.find_one({ 'approved' : 1 , 'recommended' : 0, 'date_to_post': today_date})
        if document:
            image_url = document['image-url']  # Assuming the image URL is stored in a field called 'image-url'
            description = document['caption']
            height = document['img-height']
            width = document['img-width']
            url = document['url-link']
            collection.update_one(
                {'url-link': url},
                {'$set': {'recommended': 1}}
            )
            return jsonify(image_url=image_url,description=description,width=width,height=height)  # Send the image URL as JSON
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
        print("Received URL:", url)
        print("approved:", approval)
        print("date:", date)
        # Here you can perform further processing or return a response
        # For example, return a success message
        database = client['Initial_database']
        collection = database['items']
        document = collection.find_one({'url-link': url})
        if document:
            # Update the description
            collection.update_one(
                {'url-link': url},
                {'$set': {'approved': approval,'date_to_post': date}}
            )

        return {'message': 'Data received successfully'}, 200
    except Exception as e:
        # Handle any exceptions that occur during processing
        print("Error:", e)
        return {'error': 'An error occurred'}, 500
 
# if __name__ == '__main__':
#     app.run(debug=True)  # Run the Flask app in debug mode