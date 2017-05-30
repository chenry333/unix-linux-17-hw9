#!/usr/bin/env python
"""
flask API for controlling linux services
"""
from service_mgmt import service_mgmt
from invalidusage import InvalidUsage
from flask import Flask, abort, request, jsonify, make_response

app = Flask(__name__)
app.debug = False

allowed_actions = ['start', 'stop', 'restart', 'status']

@app.errorhandler(InvalidUsage)
def invalid_request(error):
    """
    Error Handler for invalid requests raising an
    InvalidUsage object.
    :type error: InvalidUsage
    :param error: InvalidUsage object with error data
    """
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/v1/services/<action>', methods=['PUT', 'GET'])
def services(action):
    """
    Services API entry point
    :type action: string
    :param action: action to perform.
                   start, stop, restart, status
    expected API json params:
        :type service: string
        :param service: name of service to perform action on
    """
    # quick action validation
    if not action in allowed_actions:
        abort(404)

    ## parse input ##
    # grab service from json payload
    try:
        service = request.json['service']
    # Exception if service payload is missing
    except Exception, err:
        # debug mode raise exception for stack trace visibility
        if app.debug:
            raise
        raise InvalidUsage(output='no json parameter service',
                           success=False, status_code=400)

    ## make our service call ##
    # call service_mgmt and obtain output and return code
    try:
        (output, success) = service_mgmt(action=action, service=service)
    except Exception, err:
        # debug mode raise exception for stack trace visibility
        if app.debug:
            raise
        # set return values to failed if exception occurs
        output = "{0}".format(err)
        success = False


    ## format and send our response back to client ##
    # generate our response
    resp = jsonify({'success': success, 'output': output})

    # generate appropriate response code based on success
    if success:
        resp.status_code = 200
    else:
        resp.status_code = 500

    return resp

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
