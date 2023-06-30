from flask import Flask, request, render_template
import boto3
import dynamodb_handler as dynamodb

app = Flask(__name__)


dynamodb_resource = boto3.resource(
   'dynamodb',
    aws_access_key_id = 'AKIA5CFUGMGXSSIMGJKI',
    aws_secret_access_key = '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',
    region_name         = 'us-east-1'
)


@app.route('/')
def root_route():
    dynamodb.create_table_movie()
    return 'Table Created'
    # return render_template("index.html")
    
@app.route('/movie', methods=['POST'])
def add_movie():

    data = request.form.to_dict()
    
    response = dynamodb.add_item_to_movie_table(int(data['id']), data['title'], data['director'])    
    
    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        return {
            'msg': 'Added successfully',
        }

    return {  
        'msg': 'Some error occcured',
        'response': response
    }
    
    
   
#  Read a movie entry
#  Route: http://localhost:8080/movie/<id>
#  Method : GET
@app.route('/movie/<int:id>', methods=['GET'])
def get_movie(id):
    response = dynamodb.get_item_from_movie_table(id)
    
    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        
        if ('Item' in response):
            return { 'Item': response['Item'] }

        return { 'msg' : 'Item not found!' }

    return {
        'msg': 'Some error occured',
        'response': response
    }
   
   
#  Update a movie entry
#  Route: http://localhost:8080/movie/<id>
#  Method : PUT
@app.route('/movie/<int:id>', methods=['PUT'])
def update_movie_table(id):

    data = request.get_json()

    # data = {
    #     'title': 'Angels And Demons',
    #     'author': 'Daniel Brown'
    # }

    response = dynamodb.update_item_in_movie_table(id, data)

    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        return {
            'msg'                : 'Updated successfully',
            'ModifiedAttributes' : response['Attributes'],
            'response'           : response['ResponseMetadata']
        }

    return {
        'msg'      : 'Some error occured',
        'response' : response
    }
    
    
#  Delete a movie entry
#  Route: http://localhost:8080/movie/<id>
#  Method : DELETE
@app.route('/movie/<int:id>', methods=['DELETE'])
def delete_item(id):
    
    response = dynamodb.delete_item_from_movie_table(id)

    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        return {
            'msg': 'Deleted successfully',
        }

    return {  
        'msg': 'Some error occcured',
        'response': response
    }    
  
   
   
if __name__ == '__main__':
    app.run(debug=True,port=8080,host='0.0.0.0')