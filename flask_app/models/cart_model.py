from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE

from flask_app.models.part_model import Part

class Cart:
    # class constructor
    def __init__(self, data):
        self.id = data['id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.owner_id = data['owner_id']
        self.part_id = data['part_id']
    
    #? ==================== CREATE ====================
    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO carts (owner_id, part_id)
            VALUES (%(owner_id)s, %(part_id)s);
        """
        connectToMySQL(DATABASE).query_db(query, data)
    
    #? ==================== READ ====================
    @classmethod
    def get_one_user(cls, data):
        query = """
            SELECT * FROM carts 
            JOIN users ON carts.owner_id = users.id
            JOIN parts ON carts.part_id = parts.id
            WHERE users.id = %(id)s;
        """

        results = connectToMySQL(DATABASE).query_db(query, data)

        if results and len(results) > 0:
            parts_in_cart = []
            for result in results:
                part = Part.get_by_part_id({'id' : result['parts.id']})
                parts_in_cart.append(part)
        else:
            return []
            
        return parts_in_cart

    #? ==================== DELETE ====================
    @classmethod
    def delete_one_part(cls, data):
        query = """
            DELETE FROM carts 
            WHERE carts.owner_id = %(owner_id)s AND carts.part_id = %(part_id)s;
        """

        connectToMySQL(DATABASE).query_db(query, data)