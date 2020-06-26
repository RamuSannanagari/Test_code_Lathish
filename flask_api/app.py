import os
import json
import socket
import time

from utility.logger import init_logger, log, metrics_logging
from flask_restplus import reqparse, Api, Resource, fields

from middleware.filesource import FilesourceMiddleware
from middleware.Databasesource import DatabasesourceMiddleware

from flask import Flask, Response, request
from flask_cors import CORS

app = Flask(__name__, static_url_path='/static/')
app.config ['CORS_HEADERS'] ='Content-Type'
Cors = CORS(app)

api = Api(app)
init_logger()

init_logger()

#Defining api models from documentation

model_400 = api.model('Errorresponse400', {'message':fields.String, 'errors':fields.Raw})
model_500 = api.model('Errorresponse400', {'message':fields.Integer, 'errors':fields.String})
model_health_200 =api.model('successResponse200',{'success':fields.Boolean,'status':fields.Integer})

log.info("AB-server api started Successfully")



filesource_parser= reqparse.RequestParser()
filesource_parser.add_argument('file_source_type', help='Application id',location='headers', required=False)


@api.route('/file_source')
@api.expect(filesource_parser)
@api.response(200, 'Successful')
@api.response(400, 'validation Error', model_400)
@api.response(500, 'Internal processing Error', model_500)

class Filesource(Resource):
    def post(self):
        return_status = None
        result = {}
        start =int(round(time.time()*1000))

        try :
            log.info("api Request Initiated")
            fp = FilesourceMiddleware(filesource_parser)
            return_status, result = fp.run(request)
            log.info("__")
        except :
            result ={}
            log.exception('Exception while submitting file processing Request')
            return_status = 500
            result['status'] =0
            result['message'] = 'Internal Error has Occurred while processing the File request'
        finally:
            resp = Response(json.dumps(result), status = return_status, mimetype ="application/json")
            #metrics_logging(request, resp, int(round(time.time() * 100 ))start)
            
        return resp





@api.route('/database')
@api.response(200, 'Successful')
@api.response(400, 'validation Error', model_400)
@api.response(500, 'Internal processing Error', model_500)
class databasesource(Resource):
    def post(self):
        return_status = None
        result = {}
        start =int(round(time.time()*1000))

        try :
            log.info("api Request Initiated")
            fp = DatabasesourceMiddleware()
            return_status, result = fp.run(request)
            log.info("__")
        except :
            result ={}
            log.exception('Exception while submitting file processing Request')
            return_status = 500
            result['status'] =0
            result['message'] = 'Internal Error has Occurred while processing the File request'

        finally:
            resp = Response(json.dumps(result), status = return_status, mimetype ="application/json")
            #metrics_logging(request, resp, int(round(time.time() * 100 ))start)
            
        return resp

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    log.info(port)
    log.info("runing ...")
    app.run(host = '127.0.0.1', port=port)