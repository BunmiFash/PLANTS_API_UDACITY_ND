

from urllib import request
from flask import Flask, jsonify, request, abort, json
from flask_cors import CORS
from .models import setup_db, Plant

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def ater_request(response):
        response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Headers','GET, POST, PATCH,DELETE')
        return response
   
    @app.route('/plants')
    def get_plants():
        page  = request.args.get('page', 1, type=int)
        start = (page - 1)*10
        # starts from index 0 as the page starts from page 1: (1 -1)*10 = 0
        end = start + 10
        # ie 10 on a page 
        plants = Plant.query.all()
        formatted_plants = [plant.format() for plant in plants]

        return jsonify({
            'success':True,
            'plants':formatted_plants[start:end],
            'total plants':len(formatted_plants)
        })

    @app.route('/plants/<int:plant_id>')  
    def get_specific_plant(plant_id):
        plant = Plant.query.filter(Plant.id==plant_id).one_or_none()
        if plant is None:
           abort(404)

        else:
            return jsonify({
                'success':True,
                'plant': plant.format()
            })

    @app.route('/plants/<int:plant_id>', methods=['PATCH'])
    def update_plant(plant_id):
        body = request.get_json()
        plant = Plant.query.filter(Plant.id==plant_id).one_or_none()
        try:            
            new_name = body.get('name', None)
            new_scientific_name = body.get('scientific_name', None)
            new_primary_color = body.get('primary_color', None)
            new_is_poisonous  = body.get('is_poisonous', None)

            
            plant.name = new_name or plant.name
            plant.scientific_name = new_scientific_name or plant.scientific_name
            plant.primary_color = new_primary_color or plant.primary_color
            if new_is_poisonous:
                plant.is_poisonous = bool(new_is_poisonous)

            plant.update()

            return jsonify({
                'success':True,
                'id': plant_id,
                'plant':plant.format()
            })

        except:
            pass
        
    @app.route('/plants', methods=['POST'])
    def create_plant():
        body = request.get_json()
        try:
            new_plant = Plant(
            name = body.get_json('name'),
            scientific_name = body.get_json('scientific_name'),
            primary_color = body.get_json('primary_color'),
            is_poisonous = body.get_json('is_poisonous')
        )
            new_plant.insert()

            page  = request.args.get('page', 1, type=int)
            start = (page - 1)*10
            # starts from index 0 as the page starts from page 1: (1 -1)*10 = 0
            end = start + 10
            # ie 10 on a page 
            plants = Plant.query.all()
            formatted_plants = [plant.format() for plant in plants]
            return jsonify({
                'success':True,
                'plants':formatted_plants[start:end],
                'total plants':len(formatted_plants)

            })
        
        except:
            abort(404)

    @app.route('/plants/<int:plant_id>', methods=['DELETE'])
    def delete_plant(plant_id):
        deleted_plant = Plant.query.filter(Plant.id==plant_id).one_or_none()

        if deleted_plant is None:
            abort(405)
        else:
            deleted_plant.delete()
            return jsonify({
                'success':True,
                'id':plant_id
            })    


    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
                'success':False,
                'error':404,
                'message':'Not Found'
            }),404


        # if plant is None:
        #     abort(404)





    return app  