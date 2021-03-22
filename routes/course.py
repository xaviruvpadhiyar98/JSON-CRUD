"""Routes for the course resource.
"""

from run import app
from flask import request, jsonify
from http import HTTPStatus
import data
import json
from datetime import datetime

json_data = data.load_data()


@app.route("/", methods=['GET'])
def root():
    return 'Hello World'

@app.route("/course/<int:id>", methods=['GET'])
def get_course(id):
    """Get a course by id.

    :param int id: The record id.
    :return: A single course (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------   
    1. Bonus points for not using a linear scan on your data structure.
    """
    # YOUR CODE HERE
    found = True
    for x in json_data:
        if x['id'] == id:
            found = False
            return jsonify(x)
    if found:
        return jsonify({"messge": f"Course {id} does not exist"}), 404
    



@app.route("/course", methods=['GET'])
def get_courses():
    """Get a page of courses, optionally filtered by title words (a list of
    words separated by commas".

    Query parameters: page-number, page-size, title-words
    If not present, we use defaults of page-number=1, page-size=10

    :return: A page of courses (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    ------------------------------------------------------------------------- 
    1. Bonus points for not using a linear scan, on your data structure, if
       title-words is supplied
    2. Bonus points for returning resulted sorted by the number of words which
       matched, if title-words is supplied.
    3. Bonus points for including performance data on the API, in terms of
       requests/second.
    """
    # YOUR CODE HERE

    try:
        page_number=int(request.args['page-number'])
    except:
        page_number = 1
    try:
        page_size=int(request.args['page-size'])
    except:
        page_size = 10
    try:
        title_words=request.args['title-words'].split(',')
    except:
        title_words = ''

    items = []
    print(title_words)

    for x in json_data:
        if title_words:
            for y in title_words:
                if y in x['title'].lower():
                    items.append(x)
        else:
            items.append(x)

    print(items, len(items))
    try:    
        if len(items) > 0:
            new_items = [items[i:i + page_size] for i in range(0, len(items), page_size)][page_number-1]
            return jsonify(new_items)
    except Exception as e:
        return jsonify({'message': 'No more pages available'}), 404
    else:
        return str(items)
    return request.args







@app.route("/course", methods=['POST'])
def create_course():
    """Create a course.
    :return: The course object (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    1. Bonus points for validating the POST body fields
    """
    # YOUR CODE HERE
    d = {
        'id': json_data[-1]['id']+1,
        "date_created": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"), 
        "date_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
    }
    request_info = request.get_json(force=True)
    d.update(request_info)
    json_data.append(d)
    data.save_data(json_data)
    return jsonify(d)


@app.route("/course/<int:id>", methods=['PUT'])
def update_course(id):
    """Update a a course.
    :param int id: The record id.
    :return: The updated course object (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    1. Bonus points for validating the PUT body fields, including checking
       against the id in the URL

    """
    # YOUR CODE HERE
    d = {
        "date_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
    }
    request_info = request.get_json(force=True)
    d.update(request_info)
    try:
        json_data[id-1] = d
        print(json_data[id-1])
        data.save_data(json_data)
        return jsonify(d)
    except Exception as e:
        return jsonify({'message': 'The id does match the payload'}), 400

@app.route("/course/<int:id>", methods=['DELETE'])
def delete_course(id):
    """Delete a course
    :return: A confirmation message (see the challenge notes for examples)
    """
    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    None
    """
    # YOUR CODE HERE
    #json_data[id-1].pop()


    # if json_data[id-1] == id:
    #     print(json_data[id-1])
    # else:
    #     print(json_data[id])

    print(json_data[id-1]['id'])
    try:
        if json_data[id-1]['id'] == id:
            print('asbhd')
            del json_data[id-1]
            data.save_data(json_data)
            return jsonify({'messge': 'The specified course was deleted'})
        else:
            return jsonify({'message': f'Course {id} does not exist'}), 404
    except Exception as e:
        return jsonify({'message': f'Course {id} does not exist'}), 404

