import sqlite3

conn = sqlite3.connect('Product_List.db')

c = conn.cursor()

c.execute("""CREATE TABLE product_list(
    product_code integer,
    product_name text,
    product_cost real
    )""")

c.execute('''
                INSERT INTO product_list (product_code, product_name, product_cost)
                VALUES
                (1, "Bread", 30),
                (2, "Butter", 20),
                (3, "Jam", 50),
                (4, "Cheese Cube", 15),
                (5, "Cottage Cheese", 90),
                (6, "Cream", 69),
                (7, "Milk", 22),
                (8, "Curd", 40),
                (9, "Ghee", 70),
                (10, "Butter Milk", 100)
                ''')

conn.commit()

conn.close()
