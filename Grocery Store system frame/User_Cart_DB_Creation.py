import sqlite3

conn = sqlite3.connect('Cart.db')

c = conn.cursor()

c.execute("""CREATE TABLE cart(
    Product_Code integer,
    Product_Name text,
    Amount integer,
    Quantity integer
    )""")

conn.commit()

conn.close()