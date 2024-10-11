from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///voting.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define the Voter and Votes Models
class Voter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    voter_id = db.Column(db.Integer, unique=True, nullable=False)
    has_voted = db.Column(db.Boolean, default=False)

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nominee = db.Column(db.String(50), nullable=False)

# Initialize the database tables
with app.app_context():
    db.create_all()

# Nominee names
nominee1 = "Nominee 1"
nominee2 = "Nominee 2"

@app.route('/', methods=['GET'])
def home():
    return render_template('vote.html', nominee1=nominee1, nominee2=nominee2)

@app.route('/vote', methods=['POST'])
def vote():
    voter_id = int(request.form['voter_id'])
    nominee = request.form['nominee']

    # Check if the voter is valid and hasn't voted
    voter = Voter.query.filter_by(voter_id=voter_id).first()

    if voter and not voter.has_voted:
        voter.has_voted = True  # Mark as voted
        db.session.commit()

        # Record the vote
        if nominee == '1':
            vote_record = Vote(nominee=nominee1)
        elif nominee == '2':
            vote_record = Vote(nominee=nominee2)

        db.session.add(vote_record)
        db.session.commit()

        message = f"Thank you for voting for {nominee1 if nominee == '1' else nominee2}!"
    else:
        message = "Invalid Voter ID or you have already voted."

    return render_template('vote.html', nominee1=nominee1, nominee2=nominee2, message=message)

@app.route('/results', methods=['GET'])
def results():
    # Count votes for each nominee
    nm1_votes = Vote.query.filter_by(nominee=nominee1).count()
    nm2_votes = Vote.query.filter_by(nominee=nominee2).count()

    if nm1_votes > nm2_votes:
        winner = nominee1
    elif nm2_votes > nm1_votes:
        winner = nominee2
    else:
        winner = "It's a tie!"

    return render_template('vote.html', nominee1=nominee1, nominee2=nominee2, nm1_votes=nm1_votes, nm2_votes=nm2_votes, winner=winner)

if __name__ == '__main__':
    app.run(debug=True)
