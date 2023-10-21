from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

class ShopItems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    category = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer)
    shopitem_img = db.Column(db.String, unique=True)


    def __init__(self, title, description, category, price, shopitem_img):
        self.title = title
        self.description = description
        self.category = category
        self.price = price
        self.shopitem_img = shopitem_img



class ShopItemsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description', 'category', 'price', 'shopitem_img')


shopitem_schema = ShopItemsSchema()
shopitems_schema = ShopItemsSchema(many=True)


# To add new shop items

@app.route('/add', methods=["POST"])
def add_shopitem():
    post_data = request.get_json()
    title = post_data.get('title')
    description = post_data.get('description')
    category = post_data.get('category')
    price = post_data.get('price')
    shopitem_img = post_data.get('shopitem_img')


    new_shopitem = ShopItems(title, description, category, price, shopitem_img)

    db.session.add(new_shopitem)
    db.session.commit()

    return jsonify(shopitem_schema.dump(new_shopitem))
    #shopitem = ShopItems.query.get(new_shopitem.id)
    # return shopitem_schema.jsonify(shopitem)

#  Query all shop items

@app.route("/shopitems", methods=["GET"])
def get_shopitems():
    all_shopitems = db.session.query(ShopItems).all()
    return jsonify(shopitems_schema.dump(all_shopitems))


# Querying a single shop item

@app.route("/get/<id>", methods=["GET"])
def get_shopitem(id):
    shopitem = ShopItems.query.get(id)
    return shopitem_schema.jsonify(shopitem)


# Querying shop items by category

@app.route("/category", methods=["GET"])
def get_shopitemcategory():
    category = request.args.get("category")
    return [
        {"title": store.title, "category": store.category, "description": store.description, "price": store.price, "id": store.id, "shopitem_img": store.shopitem_img}
        for store in ShopItems.query.filter(ShopItems.category.startswith(category)).all()
    ]


# Querying shop items by id

@app.route("/id", methods=["GET"])
def get_shopitemid():
    shopitemid = request.args.get("id")
    return [
        {"title": store.title, "category": store.category, "description": store.description, "price": store.price, "id": store.id, "shopitem_img": store.shopitem_img}
        for store in ShopItems.query.filter(ShopItems.id).all()
    ]

# Update a shop item

@app.route("/update/<id>", methods=["PUT"])
def shopitem_update(id):
    put_data = request.get_json()
    title = put_data.get('title')
    description = put_data.get('description')
    category = put_data.get('category')
    price = put_data.get('price')
    shopitem_img = put_data.get('shopitem_img')

    shopitem_update = db.session.query(ShopItems).filter(ShopItems.id == id).first()
    if title != None: 
        shopitem_update.title = title
    if description != None: 
        shopitem_update.description = description
    if category != None: 
        shopitem_update.category = category
    if price != None: 
        shopitem_update.price = price
    if shopitem_img != None: 
        shopitem_update.shopitem_img = shopitem_img

    db.session.commit()
    return jsonify(shopitem_schema.dump(shopitem_update))

# Delete a shop item

@app.route("/delete/<id>", methods=["DELETE"])
def shopitem_delete(id):
    shopitem = ShopItems.query.get(id)
    db.session.delete(shopitem)
    db.session.commit()

    return "Shop Item was successfully deleted"

if __name__ == '__main__':
    app.run(debug=True)

