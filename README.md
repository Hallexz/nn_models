
# nn_models API

This is a RESTful API built with FastAPI for a Neural network.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/social-media-api.git


2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Start the server:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

## Endpoints

### User Management

#### Register a new user

- **Method**: `POST`
- **Path**: `/users/`
- **Description**: Register a new user in the system.
- **Request Body**: A `User` object with `username`, `email`, and `password` fields.
- **Response**: The created `User` object without the password.

#### Get a user by ID

- **Method**: `GET`
- **Path**: `/users/{user_id}`
- **Description**: Retrieve information about a user by their ID.
- **Path Parameter**: `user_id` - The ID of the user.
- **Response**: The `User` object without the password.

### Post Management

#### Create a new post

- **Method**: `POST`
- **Path**: `/posts/`
- **Description**: Create a new post.
- **Request Body**: A `Post` object with `user_id`, `text`, and optional `media` fields.
- **Response**: The created `Post` object.

#### Get a post by ID

- **Method**: `GET`
- **Path**: `/posts/{post_id}`
- **Description**: Retrieve a post by its ID.
- **Path Parameter**: `post_id` - The ID of the post.
- **Response**: The `Post` object.

#### Like a post

- **Method**: `POST`
- **Path**: `/posts/{post_id}/like`
- **Description**: Like a post.
- **Path Parameter**: `post_id` - The ID of the post.
- **Request Body**: A `User` object with the `user_id` field.
- **Response**: The updated `Post` object.

#### Comment on a post

- **Method**: `POST`
- **Path**: `/posts/{post_id}/comment`
- **Description**: Comment on a post.
- **Path Parameter**: `post_id` - The ID of the post.
- **Request Body**: A `Comment` object with `user_id` and `text` fields.
- **Response**: The updated `Post` object.

#### Repost a post

- **Method**: `POST`
- **Path**: `/posts/{post_id}/repost`
- **Description**: Repost a post.
- **Path Parameter**: `post_id` - The ID of the post.
- **Request Body**: A `User` object with the `user_id` field.
- **Response**: The updated `Post` object.

## Data Models

### User

```python
class User(BaseModel):
    id: Optional[str] = None
    username: str
    email: str
    password: str
    created_at: Optional[datetime] = None
```

### Post

```python
class Post(BaseModel):
    id: Optional[str] = None
    user_id: str
    text: str
    media: List[str] = []
    likes: List[str] = []
    comments: List[dict] = []
    reposts: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
```

### Comment

```python
class Comment(BaseModel):
    user_id: str
    text: str
    created_at: Optional[datetime] = None
```

