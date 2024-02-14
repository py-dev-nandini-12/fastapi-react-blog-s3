import os

from botocore.exceptions import NoCredentialsError
from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, Form
from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from sqlalchemy import create_engine
import boto3

DATABASE_URL = "postgresql://nandinichatterjee:postgresql_tutorial@localhost/events"
S3_BUCKET = "hello-blog"
S3_REGION = "eu-west-2"
S3_ACCESS_KEY = "AKIA5F6QMSI4SNBMJZEZ"
S3_SECRET_KEY = "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"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class BlogPost(Base):
    __tablename__ = 'blog_posts'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    image_url = Column(String(255), nullable=True)  # Add a new column for image URL


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set this to the appropriate origins in a production environment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def upload_to_s3(file):
    s3 = boto3.client(
        's3',
        aws_access_key_id=S3_ACCESS_KEY,
        aws_secret_access_key=S3_SECRET_KEY,
        region_name=S3_REGION
    )
    try:
        s3.upload_fileobj(file.file, S3_BUCKET, file.filename, ExtraArgs={'ContentType': 'image/jpeg'})
        return f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{file.filename}"
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail='S3 credentials not available.')


@app.post("/api/upload_image")
async def upload_image(file: UploadFile = File(...)):
    image_url = upload_to_s3(file)
    return {'message': f'Image uploaded successfully,image url: {image_url}.'}


@app.post("/api/save_post")
async def save_post(title: str = Form(...), content: str = Form(...), image_url: str = Form(...),
                    db: Session = Depends(get_db)):
    if title is None or content is None:
        raise HTTPException(status_code=422, detail='Title and content are required')

    post = BlogPost(title=title, content=content, image_url=image_url)

    # Save the post
    db.add(post)
    db.commit()

    return {'message': 'Post saved successfully.'}


@app.get("/api/read_post/{post_id}")
async def read_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    if post:
        return {'title': post.title, 'content': post.content, 'image_url': post.image_url}
    else:
        raise HTTPException(status_code=404, detail='Post not found.')


@app.delete("/api/delete_post/{post_id}")
async def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    if post:
        # Delete the post in the database
        db.delete(post)
        db.commit()

        return {'message': 'Post deleted successfully.'}
    else:
        raise HTTPException(status_code=404, detail='Post not found.')


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8080)
