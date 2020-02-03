def generate_id(N):
    import random
    import string
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))


def generate_message(username, email, id, mail, app):
    from flask_mail import Message

    msg = Message("Welcome to Gooday Airlines", recipients=[email])
    msg.body = f'''Hello, {username}
    Thank you for registering to Gooday Airlines. I hope you enjoy our service in the future.
    Your Frequent Flyer ID is {id}. Please save this ID somwhere since you would use
    this everytime you redeem your points. '''

    with app.open_resource("static/img/logo.png") as fp:
        msg.attach("image.png", "image/png", fp.read())

    mail.send(msg)
