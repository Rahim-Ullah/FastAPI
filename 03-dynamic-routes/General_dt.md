| Python type | Example                    |
| ----------- | -------------------------- |
| `str`       | `"Rahim"`                  |
| `int`       | `25`                       |
| `float`     | `72.5`                     |
| `bool`      | `True`                     |
| `list`      | `[1, 2, 3]`                |
| `dict`      | `{"name": "Rahim"}`        |
| `Optional`  | value may or may not exist |

## Why a nuber in url is allowed even if the function return type is a string? but the string is not allowed if the function return type is a number?
in this case 
@app.get("/products/{product_id}")
def get_product(product_id: int):
    return {"product_id": product_id}

entering abc like somthing char weill be invalid but if we replace the product_id with name then why we are allowed to insert both number and string
#### The reason 
This happens because of Python data types and how FastAPI automatically validates your input data.
When you change the variable name, it isn't the name itself that alters the rules—it is the type hint (: int or : str) attached to it.
Here is a direct comparison of how FastAPI treats both scenarios:

| Code Snippet | Accepted Inputs | Rejected Inputs | Why? |
|---|---|---|---|
| product_id: int | 123, 5 | abc, iphone | Explicitly restricted to whole numbers only. |
| name: str (or name) | iphone, abc, 123, 5 | None | Strings accept any sequence of characters, including numbers. |

## Why Numbers are Allowed in a String (str)
In computer programming, a string is just text. The character "1" is treated as text, not a mathematical number.

* When you type localhost:8000/products/abc into your browser, FastAPI reads "abc" as a string.
* When you type localhost:8000/products/123, FastAPI reads "123" as a string of text containing three digits. Since digits are valid text characters, it passes validation perfectly.

------------------------------
## How to restrict a path parameter to ONLY letters (no numbers)
If you want a variable like name to strictly reject numbers, you can use FastAPI's Query or Path validation with regular expressions (regex):

from fastapi import Path

@app.get("/products/{name}")
def get_product(name: str = Path(regex="^[a-zA-Z]+$")):
    return {"product_name": name}


* With this setup, entering /products/123 will now throw a 422 Unprocessable Entity validation error, just like the integer did!


