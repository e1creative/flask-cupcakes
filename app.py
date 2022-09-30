"""Flask app for Cupcakes"""

from flask import Flask, request, render_template, redirect, flash, session, jsonify
# from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# debug = DebugToolbarExtension(app)

connect_db(app)
# db.create_all()

@app.route('/')
def add_cupcake():
    """Render the home page, which will show a list of cupcakes and include an add cupcake form through JS"""
    return render_template('index.html')

@app.route('/api/cupcakes')
def list_cupcakes():
    """Retrieve all cupcakes"""

    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]

    return jsonify(cupcakes=all_cupcakes)


@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """Create new cupcake"""

    # retrieve the image field to see if it was left blank
    # if it was left blank, set the "image" variable equal to None
    # if we don't set the variable equal to None, our Cupcake object
    # will insert an empty string into our databse.  The only way
    # for the default value (set up in our models) to kick in is to
    # pass a None value to our new Cupcake object.
    if request.json['image'] == "":
        image = None
    else:
        image = request.json['image']

    cupcake = Cupcake(flavor=request.json['flavor'], size=request.json['size'], rating=request.json['rating'], image=image)

    db.session.add(cupcake)
    db.session.commit()

    # cupcake.serialize() is an instance method that we defined
    # it will also return the ID of the newly created cupcake
    return (jsonify(cupcake=cupcake.serialize()), 201)


@app.route('/api/cupcakes/<int:id>')
def show_cupcake(id):
    """Show a cupcake"""

    cupcake = Cupcake.query.get_or_404(id)

    return jsonify(cupcake=cupcake.serialize())


@app.route('/api/cupcakes/<int:id>', methods=['PATCH'])
def update_cupcake(id):
    """Update a cupcake"""

    cupcake = Cupcake.query.get_or_404(id)

    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)

    db.session.commit()
    
    return jsonify(cupcake=cupcake.serialize())


@app.route('/api/cupcakes/<int:id>', methods=['DELETE'])
def delete_cupcake(id):
    """Delete a cupcake"""
    cupcake = Cupcake.query.get_or_404(id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="cupcake deleted")