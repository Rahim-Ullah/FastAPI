<!-- A simple question answer -->
# Why main and app?
We use main and app simply because they are the community conventions and industry standards. Python doesn't require these names at all; developers just use them because they make code instantly readable to others.
Think of it like naming the front door of a building: you can name it anything, but calling it "Main Entrance" helps everyone find it immediately.
Here is why those two specific words became the standard:
## 1. Why main for the file?
In the programming world, main represents the starting point of an application.

* In languages like C, C++, and Java, the code must have a function explicitly named main() or it won't run.
* While Python doesn't force this rule, Python developers carried over the tradition. Naming your entry file main.py tells any developer looking at your project: "Start reading the code here."

## 2. Why app for the instance?

```txt
The word app is just a clean, short abbreviation for Application.
When you write app = FastAPI(), you are creating the core object that represents your entire web application. While you could technically name it pizza = FastAPI(), writing uvicorn main:pizza looks confusing. app keeps things obvious.
------------------------------
## You can name them absolutely anything!
To prove that Python and FastAPI don't care about these names, look at this completely valid alternative:

   1. Imagine you rename your file to server.py.
   2. Inside that file, you write your instance like this:
   ```
   
   ```python
      my_api = FastAPI()
   ```

   
   
To run this setup, you simply change your Uvicorn command to match your custom names:

```bash
uvicorn server:my_api --reload
```

This works perfectly fine, but stick to main:app for your main projects so that tutorials, AI assistants, and team members can understand your setup instantly without needing an explanation!