# lib/department.py

from __init__ import CURSOR, CONN


class Department:

    # Dictionary to cache objects saved to the database
    all = {}

    def __init__(self, name, location, id=None):
        self.id = id
        self.name = name
        self.location = location

    def __repr__(self):
        return f"<Department {self.id}: {self.name}, {self.location}>"

    @classmethod
    def create_table(cls):
        """Create a table to store Department instances"""
        sql = """
            CREATE TABLE IF NOT EXISTS departments (
                id INTEGER PRIMARY KEY,
                name TEXT,
                location TEXT
            );
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """Drop the departments table"""
        sql = "DROP TABLE IF EXISTS departments;"
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """Insert a new row for this instance and cache it"""
        sql = "INSERT INTO departments (name, location) VALUES (?, ?);"
        CURSOR.execute(sql, (self.name, self.location))
        CONN.commit()

        # Set id and cache instance
        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, name, location):
        """Create a new Department instance and save it"""
        department = cls(name, location)
        department.save()
        return department

    def update(self):
        """Update the database row corresponding to this instance"""
        sql = "UPDATE departments SET name = ?, location = ? WHERE id = ?;"
        CURSOR.execute(sql, (self.name, self.location, self.id))
        CONN.commit()

    def delete(self):
        """Delete the database row and remove instance from cache"""
        sql = "DELETE FROM departments WHERE id = ?;"
        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        # Remove from dictionary
        del type(self).all[self.id]

        # Reset id
        self.id = None

    @classmethod
    def instance_from_db(cls, row):
        """Return a Department instance corresponding to a database row"""
        department = cls.all.get(row[0])
        if department:
            # Update attributes in case they were modified locally
            department.name = row[1]
            department.location = row[2]
        else:
            # Not in cache, create and store
            department = cls(row[1], row[2])
            department.id = row[0]
            cls.all[department.id] = department
        return department

    @classmethod
    def get_all(cls):
        """Return a list of all Department instances in the database"""
        sql = "SELECT * FROM departments;"
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        """Return Department instance matching a given primary key"""
        sql = "SELECT * FROM departments WHERE id = ?;"
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        """Return Department instance matching a given name"""
        sql = "SELECT * FROM departments WHERE name = ?;"
        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None
