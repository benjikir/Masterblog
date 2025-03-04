from flask import Flask, render_template, request, redirect, url_for
import json
import random

app = Flask(__name__)

BLOG_POSTS_FILE = "blog_posts.json"  # Constant for the filename

def load_blog_posts():
    """Loads blog posts from the blog_posts.json file."""
    try:
        with open(BLOG_POSTS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: blog_posts.json not found.  Creating an empty list.")
        return []  # Return an empty list if the file doesn't exist
    except json.JSONDecodeError:
        print("Error: blog_posts.json contains invalid JSON. Returning an empty list.")
        return []

def save_blog_posts(posts):
    """Saves blog posts to the blog_posts.json file."""
    try:
        with open(BLOG_POSTS_FILE, "w") as f:
            json.dump(posts, f, indent=4)  # Use indent for readability
    except IOError:
        print(f"Error: Could not write to {BLOG_POSTS_FILE}")


@app.route('/')
def index():
    """Renders the index page with blog posts."""
    blog_posts = load_blog_posts()  # Load blog posts from the JSON file
    return render_template('index.html', posts=blog_posts)  # Pass posts to the template

@app.route('/add', methods=['GET', 'POST'])
def add():
    blog_posts = load_blog_posts()
    if request.method == 'POST':
        title = request.form.get('title')  # Correct way to get form data, as suggested in task.
        content = request.form.get('content')  # Correct way to get form data, as suggested in task.
        # Add the code that handles adding a new blog
        new_id = random.randint(100, 999)
        while any(post['id'] == new_id for post in blog_posts):
            new_id = random.randint(100, 999)

        new_post = {
            'id': new_id,
            'title': title,
            'content': content
        }
        blog_posts.append(new_post)
        save_blog_posts(blog_posts) # Save the updated list to the JSON file

        return redirect(url_for('index'))  # Redirect to the home page

    return render_template('add.html')  # Render the form on GET requests


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """Deletes a blog post."""
    blog_posts = load_blog_posts()  # Load the current blog posts
    # Find the blog post with the given id and remove it from the list
    blog_posts = [post for post in blog_posts if post['id'] != post_id] # List comprehension to create new list without post to be deleted

    save_blog_posts(blog_posts)  # Save the updated blog posts to the JSON file
    return redirect(url_for('index'))  # Redirect back to the home page


if __name__ == '__main__':
    app.run(debug=True)