from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE

class Part:

    # class constructor
    def __init__(self, data):
        self.id = data['id']
        self.component = data['component']
        self.manufacturer = data['manufacturer']
        self.name = data['name']
        self.price = data['price']
        self.used = data['used']
        self.img = data['img']
        self.owner_id = data['owner_id']
    
    #? ==================== CREATE ====================
    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO parts (component, manufacturer, name, price, used, img, owner_id)
            VALUES (%(component)s, %(manufacturer)s, %(name)s, %(price)s, %(used)s, %(img)s, %(owner_id)s);
        """
        connectToMySQL(DATABASE).query_db(query, data)
    
    #? ==================== READ ====================
    @classmethod
    def get_one_user(cls, data):
        query = """
            SELECT * FROM parts
            JOIN users ON parts.owner_id = users.id
            WHERE users.id = %(id)s;
        """

        results = connectToMySQL(DATABASE).query_db(query, data)

        found_parts = []

        if results:
            for result in results:  
                found_parts.append(cls(result))
        else: 
            return False
        
        return found_parts

    @classmethod
    def get_by_part_id(cls, data):
        query = """
            SELECT * FROM parts
            WHERE parts.id = %(id)s;
        """

        results = connectToMySQL(DATABASE).query_db(query, data)

        if results:
            return cls(results[0])
        else: 
            return False

    @classmethod
    def get_all(cls, data):
        query = """
            SELECT * FROM parts;
        """

        results = connectToMySQL(DATABASE).query_db(query, data)

        found_parts = []

        if results:
            for result in results:  
                found_parts.append(cls(result))
        else: 
            return False
    
    #* ========== SELECT DIFFERENT PARTS ==========
    # CPU
    @classmethod
    def display_cpus(cls):
        query = """
            SELECT * FROM parts WHERE parts.component = 'CPU';
        """

        results = connectToMySQL(DATABASE).query_db(query)

        if results and len(results) > 0:
            found_cpus = []
            for result in results:
                found_cpus.append(cls(result))
        else: 
            return False
        
        return found_cpus

    # Motherboard
    @classmethod
    def display_motherboards(cls):
        query = """
            SELECT * FROM parts WHERE parts.component = 'Motherboard';
        """

        results = connectToMySQL(DATABASE).query_db(query)

        if results and len(results) > 0:
            found_motherboards = []
            for result in results:
                found_motherboards.append(cls(result))
        else: 
            return False
        
        return found_motherboards

    # GPU
    @classmethod
    def display_gpus(cls):
        query = """
            SELECT * FROM parts WHERE parts.component = 'GPU';
        """

        results = connectToMySQL(DATABASE).query_db(query)

        if results and len(results) > 0:
            found_gpus = []
            for result in results:
                found_gpus.append(cls(result))
        else: 
            return False
        
        return found_gpus

    # Memory
    @classmethod
    def display_memories(cls):
        query = """
            SELECT * FROM parts WHERE parts.component = 'Memory';
        """

        results = connectToMySQL(DATABASE).query_db(query)

        if results and len(results) > 0:
            found_memories = []
            for result in results:
                found_memories.append(cls(result))
        else: 
            return False
        
        return found_memories

    # Storage
    @classmethod
    def display_storages(cls):
        query = """
            SELECT * FROM parts WHERE parts.component = 'Storage';
        """

        results = connectToMySQL(DATABASE).query_db(query)

        if results and len(results) > 0:
            found_storages = []
            for result in results:
                found_storages.append(cls(result))
        else: 
            return False
        
        return found_storages
    
    # Cooler
    @classmethod
    def display_coolers(cls):
        query = """
            SELECT * FROM parts WHERE parts.component = 'Cooler';
        """

        results = connectToMySQL(DATABASE).query_db(query)

        if results and len(results) > 0:
            found_coolers = []
            for result in results:
                found_coolers.append(cls(result))
        else: 
            return False
        
        return found_coolers

    # Power
    @classmethod
    def display_powers(cls):
        query = """
            SELECT * FROM parts WHERE parts.component = 'Power';
        """

        results = connectToMySQL(DATABASE).query_db(query)

        if results and len(results) > 0:
            found_powers = []
            for result in results:
                found_powers.append(cls(result))
        else: 
            return False
        
        return found_powers
    
    #? ==================== UPDATE ====================
    @classmethod
    def update_one(cls, data):
        query = """
            UPDATE parts 
            SET component = %(component)s, manufacturer = %(manufacturer)s, name = %(name)s, price = %(price)s, used = %(used)s, img = %(img)s 
            WHERE parts.id = %(id)s;
        """
        connectToMySQL(DATABASE).query_db(query, data)

    #? ==================== DELETE ====================
    @classmethod
    def delete_one(cls, data):
        query = """
            DELETE FROM parts WHERE parts.id = %(id)s;
        """

        connectToMySQL(DATABASE).query_db(query, data)

    #? ==================== VALIDATION ====================
    @staticmethod
    def validate(data):
        is_valid = True

        #! ========== Checking COMPONENT ==========
        # Manufacturer should not be void
        if data['component'] == 'Choose...':
            flash("Component should not be blank!", "component")
            is_valid = False

        #! ========== Checking MANUFACTURER ==========
        # Manufacturer should not be void
        if len(data['manufacturer']) == 0:
            flash("Manufacturer should not be blank!", "component")
            is_valid = False

        #! ========== Checking NAME ==========
        # Name should not be void
        if len(data['name']) == 0:
            flash("Name should not be blank!", "component")
            is_valid = False

        #! ========== Checking PRICE ==========
        # Price should not be empty
        if len(data['price']) == 0:
            flash("Price should not be blank!", "component")
            is_valid = False
        
        # return true once passed all checks
        return is_valid
