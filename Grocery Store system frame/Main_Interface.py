from tkinter import *
from Add_product_to_DB_maually_Function import *

# object of TK()
root = Tk()
root.geometry("1920x1080")
root.title("Grocery Store")


#icon

p1 = PhotoImage(file = 'logo.png')
root.iconphoto(True, p1)


#******************************************* raise funtion logic *******************************************************

def raise_frame(frame):
	frame.tkraise()

home_frame = LabelFrame(root, text = "HOME",fg="White",bg="black")
newWindow2 = LabelFrame(root, text = "Bill",fg="White",bg="black")


for frame in (home_frame,newWindow2):
	frame.grid(row=0, column=0, sticky='news')

# Define image
bg1 = PhotoImage(file="bg.png")

# Create a canvas home frame

My_canvas2 = Canvas(newWindow2, width=1920, height=1080)
My_canvas2.pack(fill="both", expand=True)

# Set image in canvas
My_canvas2.create_image(0,0, image=bg1 ,anchor="nw")	

#******************************************* display logic *******************************************************
def display():
	recordID = product_Code_Input.get()
	conn = sqlite3.connect('Product_List.db')
	c = conn.cursor()
	c.execute("SELECT * FROM product_list WHERE oid = " + recordID)
	records = c.fetchall()
	for record in records:
		product_Name_Input.insert(0, record[1])
		product_Cost_Input.insert(0, record[2])

	conn.commit()
	conn.close()

# calculate logic
def calculate():
	a = Quantity_Input.get()
	b = product_Cost_Input.get()
	c = float(a) * float(b)
	Total_Amount_Display.insert(0, c)

# add_product_to_cart logic
def add_product_to_cart():
	conn = sqlite3.connect('Cart.db')
	c = conn.cursor()
	c.execute("INSERT INTO cart VALUES(:Product_Code, :Product_Name, :Amount ,:Quantity)",
				{
					'Product_Code': product_Code_Input.get(),
					'Product_Name': product_Name_Input.get(),
					'Amount': Total_Amount_Display.get(),
					'Quantity': Quantity_Input.get()
				}
				)
	conn.commit()
	conn.close()

	product_Code_Input.delete(0, END)
	product_Cost_Input.delete(0, END)
	product_Name_Input.delete(0, END)
	Total_Amount_Display.delete(0, END)
	Quantity_Input.delete(0, END)

# bill logic

# def bill():

def show():
	conn = sqlite3.connect('Cart.db')
	c = conn.cursor()
	c.execute("SELECT * ,oid from cart")
	records = c.fetchall()

	# loop
	global printRecord
	printRecord = ''
	for record in records:
		printRecord = printRecord + record[1] + "\t\t" + str(record[2]) + "\t" + "\n"

	global printLabel	
	printLabel = My_canvas2.create_text(1000,100 ,text=printRecord,
					 font=("Arial", 20, "bold"))
	# printLabel.config(text=printRecord)

	conn.commit()
	conn.close()
	
show()

# Calculating and Printing the Total Bill
def receipt():
			conn = sqlite3.connect('Cart.db')
			c = conn.cursor()
			c.execute("SELECT *, oid from cart")
			records = c.fetchall()

			# Loop
			# For Total Amount of Products
			global totalBill
			totalAmount = 0
			for record in records:
				if record[2] == '':
					continue
				totalAmount = totalAmount + float(record[2])

			totalBill = totalAmount

			totalLabel1 = My_canvas2.create_text(950,150, text="Total Bill: " + "\t \t" + "₹ " + str(totalBill),
							   font=("Arial", 15, "bold"))
			

			# For Total Product Count
			global totalQuantity	
			totalQuantity = 0
			for record in records:
				if record[3] == '':
					continue
				totalQuantity = totalQuantity + float(record[3])

			totalLabel2 = My_canvas2.create_text(950,200, text="Total Products Purchased: " + "\t" + str(totalQuantity),
							   font=("Arial", 15, "bold"))


			conn.commit()
			conn.close()

receipt()

def delete_cart():
	conn = sqlite3.connect('Cart.db')
	c = conn.cursor()
	for i in range(0, 20):
		c.execute("DELETE FROM cart WHERE Product_Code = " + str(i))
		# c.execute("DELETE FROM cart WHERE Product_Code in (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15)")
	# printLabel.config(text="")
	conn.commit()
	conn.close()

def printReceipt():
    return

# Taking Paid Input and Displaying Balance Value

paidLabel = My_canvas2.create_text(800,350, text="Paid Amount: ", font=("Times", 20))


paidLabel_Input = Entry(newWindow2, width=30, borderwidth=5)
paidLabel_Input.place(x=1000,y=340)

balanceLabel = My_canvas2.create_text(800,390, text="Balance: ", font=("Times", 20))


balanceLabel_Input = Entry(newWindow2, width=30, borderwidth=5)
balanceLabel_Input.place(x=1000,y=380)


# Function for Calculating Balance

def balanceCalculation():
    paid = float(paidLabel_Input.get())
    conn = sqlite3.connect('Cart.db')
    c = conn.cursor()
    c.execute("SELECT *, oid from cart")
    records = c.fetchall()

    # Loop

    total = 0.0
    for record in records:
        if record[2] == '':
            continue
        total = total + float(record[2])

    totalBill = total
    balance = paid - totalBill
    balanceLabel_Input.insert(0, balance)

# Calculate Balance Button Creation

calculateBalanceButton = Button(newWindow2, text="CALCULATE BALANCE", font="Times",
                                command=balanceCalculation,
                                borderwidth=5)
calculateBalanceButton.place(x=890,y=420)

# "Thank You" Label

# thank_you_Label = Label(newWindow2,
#                         text="THANK YOU AND VISIT AGAIN!",
#                         font=("Arial", 12, "bold italic underline"),
#                         bg="gold",
#                         fg="black")
# thank_you_Label.grid(row=7, column=0, columnspan=4, pady=20)

# # Print Receipt, Delete Cart, Back Button Creation

printReceipt_button = Button(newWindow2, text="PRINT RECEIPT", font="Times", command=printReceipt, borderwidth=5)
printReceipt_button.place(x=920,y=470)

# delete_Cart_button = Button(newWindow2, text="DELETE CART", font="Times", command=delete_cart, borderwidth=5,
#                             bg="light yellow")
# delete_Cart_button.grid(row=9, column=3, pady=15, padx=10)

back_button = Button(newWindow2, text="BACK", font="Times", command=lambda:[raise_frame(home_frame)], borderwidth=5)
back_button.place(x=940,y=520)

# *******************************************home frame*******************************************
# Define image

bg = PhotoImage(file="bg.png")

# Create a canvas home frame
My_canvas = Canvas(home_frame, width=1920, height=1080)
My_canvas.pack(fill="both", expand=True)

# Set image in canvas
My_canvas.create_image(0,0, image=bg ,anchor="nw")

main_Label = My_canvas.create_text(950,50,
				 text="Grocery Store System",
				 font=("Arial", 65, "bold italic underline")
				 )


product_Code_Label = My_canvas.create_text(800,165, text="Product Code: ", font=("Times", 20))

product_Code_Input = Entry(home_frame, width=30, borderwidth=5)
product_Code_Input.place(x=960,y=155)

display_button = Button(home_frame, text="DISPLAY PRODUCT DETAILS", font="Times", command=display, borderwidth=5)
display_button.place(x=830,y=205)

product_Name_Label = My_canvas.create_text(790,280 , text="Product Purchased: ", font=("Times", 20))

product_Name_Input = Entry(home_frame, width=30, borderwidth=5)
product_Name_Input.place(x=960,y=268)

product_Cost_Label = My_canvas.create_text(800,340, text="Product Cost: ", font=("Times", 20))

product_Cost_Input = Entry(home_frame, width=30, borderwidth=5)
product_Cost_Input.place(x=960,y=330)

Quantity = My_canvas.create_text(820,400, text="Quantity: ", font=("Times", 20))

Quantity_Input = Entry(home_frame, width=30, borderwidth=5)
Quantity_Input.place(x=960,y=390)

calculate_button = Button(home_frame, text="CALCULATE", font="Times", command=calculate, borderwidth=5)
calculate_button.place(x=900,y= 450)

Total_Amount = My_canvas.create_text(730,530 ,text="Total Amount of this Product: ", font=("Times", 20))

Total_Amount_Display = Entry(home_frame, width=30, borderwidth=5)
Total_Amount_Display.place(x=960,y=520)

add_Product_button = Button(home_frame, text="ADD TO CART", font="Times", command=add_product_to_cart, borderwidth=5)
add_Product_button.place(x=895,y=565)

bill_button = Button(home_frame, text="DISPLAY BILL", font="Times", command=lambda:[raise_frame(newWindow2),show(),receipt()], borderwidth=5)
bill_button.place(x=895,y=620)

exit_app_button = Button(home_frame, text="EXIT", font="Times", command=home_frame.quit, borderwidth=5,)
exit_app_button.place(x=930,y=680)

admin_access_button = Button(home_frame, text="ADMIN", font="Times", command=add_product_to_database, borderwidth=5,)
admin_access_button.place(x=1800,y=10)



# ******************************************* display frame *******************************************

delete_Cart_button = Button(newWindow2, text=" DELETE CART", font="Times", command=lambda:[raise_frame(home_frame),delete_cart()], borderwidth=5)
delete_Cart_button.place(x=890,y=230)

thank_you_Label = My_canvas2.create_text(950,300 ,text="THANK YOU AND VISIT AGAIN!",
						font=("Arial", 10, "bold italic underline"))


raise_frame(home_frame)

root.mainloop()
