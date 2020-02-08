from flaskapp import app, db

if (__name__ == "__main__"):
    import test
    app.run(debug=True)
    db.drop_all() # remember to delete this line once you are done