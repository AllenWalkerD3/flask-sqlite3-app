import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True, help="This field cannot be left blank"
    )

    @classmethod
    def get_item_by_name(cls, name):
        connection = sqlite3.connect("mydb.db")
        cursor = connection.cursor()

        query = "select * from tbl_item where name=?"

        result = cursor.execute(query, (name,))

        row = result.fetchone()
        connection.close()
        if row:
            return {"id": row[0], "name": row[1], "price": row[2]}
        return None

    @classmethod
    def insert(cls, name, price):
        connection = sqlite3.connect("mydb.db")
        cursor = connection.cursor()
        query = "insert into tbl_item values (NULL, ?, ?)"
        cursor.execute(query, (name, price))
        connection.commit()
        connection.close()

    @classmethod
    def update(cls, name, price):
        connection = sqlite3.connect("mydb.db")
        cursor = connection.cursor()
        query = "update tbl_item set price=? where name=?"
        cursor.execute(query, (price, name))
        connection.commit()
        connection.close()


    @jwt_required()
    def get(self, name):
        item = self.get_item_by_name(name)
        if item:
            return {"item": item}
        return {"message": "Item not found"}, 404

    def post(self, name):

        item = self.get_item_by_name(name)
        if item:
            return {"message": "A user with that item already exist"}, 400

        data = Item.parser.parse_args()
        try:
            self.insert(name, data["price"])
        except:
            return {"message": "An Error occurred inserting the item."}, 500
        return {"item": self.get_item_by_name(name)}, 201

    def put(self, name):

        item = self.get_item_by_name(name)

        data = Item.parser.parse_args()
        try:
            if not item:
                self.insert(name, data["price"])
            else:
                self.update(name, data["price"])
        except:
            return {"message": "An Error occurred."}, 500

        return {"item": self.get_item_by_name(name)}

    def delete(self, name):
        connection = sqlite3.connect("mydb.db")
        cursor = connection.cursor()

        query = "delete from tbl_item where name=?"

        cursor.execute(query, (name,))
        connection.commit()
        connection.close()
        return {"message": "Item deleted"}


class ItemList(Resource):
    @classmethod
    def get_items(cls):
        connection = sqlite3.connect("mydb.db")
        cursor = connection.cursor()

        query = "select * from tbl_item"

        result = cursor.execute(query)

        rows = result.fetchall()
        connection.close()
        items = [{"id": row[0], "name": row[1], "price": row[2]} for row in rows]
        return items

    def get(self):
        return {"items": self.get_items()}
