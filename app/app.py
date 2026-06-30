from fastapi import FastAPI, HTTPException
from app.schemas import CreatePost

app= FastAPI()

### { GET }

@app.get("/hello-world")
def hello_world():                       # Function name should be same or similar to the decorator
    return {"message": "Hello World"}    # Should be in Pydantic Format

text_posts = {
    1:  { "title": "New Post", "content": "Cool test post" },
    2:  { "title": "Python Tip", "content": "Use list comprehensions for cleaner loops." },
    3:  { "title": "Daily Motivation", "content": "Consistency beats intensity every time." },
    4:  { "title": "Fun Fact", "content": "The first computer bug was an actual moth found in a Harvard Mark II. " },
    5:  { "title": "Update", "content": "Just launched my new project! Excited to share more soon." },
    6:  { "title": "Tech Insight", "content": "Async I0 in Python can massively speed up I/0-bound tasks." },
    7:  { "title": "Quote", "content": "Programs must be written for people to read, and only incidentally for macl" },
    8:  { "title": "Weekend Plans", "content": "Might finally clean up my GitHub repos ... or just play some Minecraf" },
    9:  { "title": "Question", "content": "What's the most underrated Python library you've ever used?" },
    10: { "title": "Mini Announcement", "content": "New video drops tomorrow-covering the weirdest Python features" }
}

@app.get("/posts")
def get_all_posts():                     # Default= None
    return ( f"Number of text_posts: {len(text_posts)}", text_posts )


## QUERY PARAMETER
@app.get("/post_limits")
# FastAPI provides AutoValidation of Query parameters types 
def get_limit_post(limit:int= None):     ## In such cases(single endpoint "/post_limits"), Passing None makes it optional and doesnt give errors if no input is passed, else if None is not passed, then passing an parameter becomes mandatory
    if limit:
        if limit>len(text_posts):
            raise HTTPException(status_code=404, detail="Limit is greater than the number of posts")
        else:
            return list(text_posts.items())[:limit]
    raise HTTPException(status_code=400, detail="Empty-limit, Input required")


## PATH PARAMETER
@app.get("/posts/{id}")
def get_id_post(id:int= None):           ## In such cases(multiple endpoints "/posts/{id}"), input is mandatory always
    if id not in text_posts:
        raise HTTPException(status_code=404, detail="Post not found")
    return text_posts.get(id)


### { POST }
@app.post("/posts")
def create_post(post: CreatePost):
    new_post= { "title": post.title, "content": post.content}
    text_posts[len(text_posts)+1]= new_post
    return new_post
## OR
#  text_posts[len(text_posts) + 1] = post.model_dump()
#  return text_posts[len(text_posts)]


### { DELETE }
@app.delete("/posts")
def delete_post(index: int):
    text_posts.pop(index)
    return get_all_posts()

### { PATCH }
@app.patch("/posts")
def patch_post(index: int, post: CreatePost):
    # text_posts[index]= post         ## NOTE: This is wrong, you just passed an entire pydantic object into an index of a dictionary ( i.e. text_posts[index]["title"], will crash ), so use .model_dump() to convert the pydantic object into a python dictionary
    text_posts[index]= post.model_dump()
    return get_all_posts()
## If an index which doesnt exists is passed, then PATCH will act as POST