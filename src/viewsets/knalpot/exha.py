from flask_restful import (
    request, 
    Resource
)
from utils.kode import run

class exharecog(Resource):
    def post(self, *args, **kwargs):
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            t = run(uploaded_file)
        return t, 200