"""
Blue Bloom Travel — Flask Application
======================================
The database only stores what users submit:
  - Bookings  (when someone fills the Book Now form)
  - Comments  (when someone leaves a review on a package)
  - Contacts  (when someone sends a message)
"""


from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector


app = Flask(__name__)
app.secret_key = "blue_bloom_secret_key"


# ── Database Connection ───────────────────────────────────────
def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Meiry1234$",      
        database="travel_agency"
    )
    return conn



#    List of packages (hardcoded here so the booking dropdown
#    always matches what's shown on the packages page) 
PACKAGES = [
    "Lantern Festival Experience",
    "Cherry Blossom Season",
    "Seoul & Busan Adventure",
    "Carnival in Rio",
    "Pyramids of Giza Experience",  
    "Harbin Ice & Snow Festival",
]



# ═══════════════════════════════════════════════════════════════
# HOME
# ═══════════════════════════════════════════════════════════════
@app.route("/")
def home():
    return render_template("index.html")



# ═══════════════════════════════════════════════════════════════
# PACKAGES — static page, no DB
# ═══════════════════════════════════════════════════════════════
""" This page shows all the travel packages.
        The packages are written directly in packages.html — not from the database.
        I pass the PACKAGES list so the comment forms know which package they belong to. 
"""

@app.route("/packages")
def packages():
    # Fetch comments from DB so each package can show its reviews
    conn   = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM comments ORDER BY created_at DESC")
    all_comments = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("packages.html", all_comments=all_comments, packages=PACKAGES)


# ═══════════════════════════════════════════════════════════════
# BOOKINGS — users submit, we save to DB
# ═══════════════════════════════════════════════════════════════

"""
This page shows the booking form.
If the user clicked "Book Now" on a package, that package
is already selected in the dropdown when the form opens.
When the user submits the form, it save the booking to the database.
"""

@app.route("/book", methods=["GET", "POST"])
def book():

    if request.method == "POST":
        package_name  = request.form["package_name"]
        name          = request.form["name"]
        email         = request.form["email"]
        travel_date   = request.form["travel_date"]
        num_travelers = request.form["num_travelers"]

        conn   = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO bookings (package_name, name, email, travel_date, num_travelers) "
            "VALUES (%s, %s, %s, %s, %s)",
            (package_name, name, email, travel_date, num_travelers)
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash("Booking submitted! We'll be in touch soon. ✈️", "success")
        return redirect(url_for("bookings"))

    # GET — pre-select the package if it came from a "Book Now" button
    selected_package = request.args.get("package", "")
    return render_template("book.html", packages=PACKAGES, selected=selected_package)



""" This one shows all bookings saved in the database."""

@app.route("/bookings")
def bookings():
    conn   = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM bookings ORDER BY created_at DESC")
    all_bookings = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("bookings.html", bookings=all_bookings)


@app.route("/bookings/delete/<int:booking_id>", methods=["POST"])
def delete_booking(booking_id):
    """Deletes one booking by ID."""
    conn   = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM bookings WHERE id = %s", (booking_id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash("Booking deleted.", "success")
    return redirect(url_for("bookings"))




"""
    This function searches my bookings by traveler name, email, or package name.
    The search term comes from the search bar on the bookings page.
"""
@app.route("/bookings/search")
def search_bookings():

    query   = request.args.get("q", "")
    results = []

    if query:
        conn   = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        search_term = f"%{query}%"
        cursor.execute(
            "SELECT * FROM bookings WHERE name LIKE %s OR email LIKE %s "
            "OR package_name LIKE %s ORDER BY created_at DESC",
            (search_term, search_term, search_term)
        )
        results = cursor.fetchall()
        cursor.close()
        conn.close()

    return render_template("bookings.html", bookings=results, query=query)


# ═══════════════════════════════════════════════════════════════
# COMMENTS — users submit per package, it's save to the DB
# ═══════════════════════════════════════════════════════════════

@app.route("/comments/add", methods=["POST"])
def add_comment():
    """Saves a comment and redirects back to the packages page."""
    package_name = request.form["package_name"]
    username     = request.form["username"]
    message      = request.form["message"]

    conn   = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO comments (package_name, username, message) VALUES (%s, %s, %s)",
        (package_name, username, message)
    )
    conn.commit()
    cursor.close()
    conn.close()

    flash("Comment posted! 💬", "success")
    return redirect(url_for("packages") + f"#{package_name.replace(' ', '-')}")


@app.route("/comments/delete/<int:comment_id>", methods=["POST"])
def delete_comment(comment_id):
    """Deletes a comment by ID."""
    conn   = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM comments WHERE id = %s", (comment_id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash("Comment deleted.", "success")
    return redirect(url_for("packages"))


"""
    This page lets the user edit a comment.
    When the user opens it, the form is already filled with the current comment.
    When the user submits the form, it saves the changes to the database.  
"""
@app.route("/comments/edit/<int:comment_id>", methods=["GET", "POST"])
def edit_comment(comment_id):

    conn   = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        username = request.form["username"]
        message  = request.form["message"]

        # It only changes the username and message — not the package or date
        cursor.execute(
            "UPDATE comments SET username=%s, message=%s WHERE id=%s",
            (username, message, comment_id)
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash("Comment updated! ✏️", "success")
        return redirect(url_for("packages"))

   # It load the current comment from the database so the form shows the existing text.
    cursor.execute("SELECT * FROM comments WHERE id = %s", (comment_id,))
    comment = cursor.fetchone()
    cursor.close()
    conn.close()

    if not comment:
        flash("Comment not found.", "error")
        return redirect(url_for("packages"))

    return render_template("edit_comment.html", comment=comment)


# ═══════════════════════════════════════════════════════════════
# FESTIVALS — fully static page
# ═══════════════════════════════════════════════════════════════

@app.route("/festivals")
def festivals():
    return render_template("festivals.html")



# ═══════════════════════════════════════════════════════════════
# CONTACT — user submits, save to DB
# ═══════════════════════════════════════════════════════════════

@app.route("/contact", methods=["GET", "POST"])
def contact():
    """GET → shows form. POST → saves message to DB."""
    if request.method == "POST":
        name    = request.form["name"]
        email   = request.form["email"]
        subject = request.form["subject"]
        message = request.form["message"]

        conn   = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO contacts (name, email, subject, message) VALUES (%s, %s, %s, %s)",
            (name, email, subject, message)
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash("Message sent! We'll get back to you soon. 📬", "success")
        return redirect(url_for("contact"))

    return render_template("contact.html")


# ═══════════════════════════════════════════════════════════════
# RUN
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app.run(debug=True)
