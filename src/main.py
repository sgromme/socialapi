from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class UserPostIn(BaseModel):
    body: str


class UserPost(UserPostIn):
    id: int


post_table = {}


@app.post("/", response_model=UserPost)
async def create_post(post: UserPostIn):
    data = post.model_dump()
    last_record_id = len(post_table)
    new_post = {**data, "id": last_record_id}
    post_table[last_record_id] = new_post
    return new_post


@app.get("/")
async def root():
    return {"message": "Hello World12"}
