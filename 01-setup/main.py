from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Pydantic model for cart item
class CartItem(BaseModel):
	item_id: int
	name: str
	quantity: int
	price: float

# In-memory cart storage (for demonstration)
cart = []


@app.get("/")
def read_root():
	return {"message": "Hello, World from main!"}
# A simple string can also be returned here just as a normal function retuning a string

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
	return {"item_id": item_id, "q": q}


@app.post("/cart/add")
def add_to_cart(item: CartItem):
	"""Add an item to the shopping cart"""
	cart.append(item.dict())
	return {
		"message": "Item added to cart successfully",
		"item": item,
		"cart_total_items": len(cart)
	}


@app.get("/cart")
def view_cart():
	"""View all items in the cart"""
	total_price = sum(item['price'] * item['quantity'] for item in cart)
	return {
		"cart": cart,
		"total_items": len(cart),
		"total_price": total_price
	}