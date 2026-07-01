# This imports Flask tools.
# Flask creates the web backend.
from flask import Flask, render_template

# This creates the Flask app.
# template_folder tells Flask where the HTML files are.
# static_folder tells Flask where CSS and JS files are.
app = Flask(
    __name__,
    template_folder="frontend",
    static_folder="frontend",
)


@app.route("/")
def dashboard():
    """Show the dashboard page."""
    # This sends index.html to the browser.
    return render_template("index.html")


# This starts the Flask app.
# debug=True helps us see errors while learning.
if __name__ == "__main__":
    app.run(debug=True)
