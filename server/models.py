from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates("name")
    def validate_name(self, key, val):
        if not val:
            raise ValueError("All authors must have a name.")
        author = db.session.query(Author.id).filter_by(name=val).first()
        if author is not None:
            raise ValueError("No two authors have the same name.")
        return val

    @validates("phone_number")
    def validate_phone_number(self, key, val):
        if len(val) != 10 or not val.isdigit():
            raise ValueError("Author phone numbers are exactly ten digits.")
        return val

    def __repr__(self):
        return f"Author(id={self.id}, name={self.name})"


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates("title")
    def validate_title(self, key, val):
        if not val:
            raise ValueError("Post must have a title.")
        options = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(opt in val for opt in options):
            raise ValueError("Post title is sufficiently clickbait-y.")
        return val

    @validates("content", "summary")
    def validate_length(self, key, val):
        if key == "content":
            if len(val) < 250:
                raise ValueError("Post content is at least 250 characters long.")
        if key == "summary":
            if len(val) > 250:
                raise ValueError("Post summary is a maximum of 250 characters.")
        return val

    @validates("category")
    def validate_category(self, key, val):
        if val != "Fiction" and val != "Non-Fiction":
            raise ValueError("Post category is either Fiction or Non-Fiction.")
        return val

    def __repr__(self):
        return f"Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})"