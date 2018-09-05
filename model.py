"""Models and database functions for Rideshare project."""

import bcrypt
from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()

##############################################################################
# Model definitions


class User(db.Model):  # pragma: no cover
    """User information."""

    __tablename__ = "users"

    # Log-in information
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(649), nullable=True)

    # Profile information
    fname = db.Column(db.String(20), nullable=True)
    lname = db.Column(db.String(20), nullable=True)
    user_gender = db.Column(db.String(20), nullable=True)
    user_bio = db.Column(db.String(160), nullable=True)
    user_profile_img = db.Column(db.String(250), nullable=True)
    user_social_media = db.Column(db.String(3000), nullable=True)
    phone_number = db.Column(db.Numeric(12), nullable=True)

    def to_json(self):  # pragma: no cover
        """Serialize data."""
        return {'user_id': self.user_id,
                'email': self.email,
                'password': self.password,
                'fname': self.fname,
                'lname': self.lname,
                'userGender': self.user_gender,
                'userBio': self.user_bio,
                'userProfileImg': self.user_profile_img,
                'userSocialMedia': self.user_social_media}


class Trip(db.Model):  # pragma: no cover
    """Trip information."""

    __tablename__ = "trips"

    trip_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    is_active = db.Column(db.Boolean)
    date_of_trip = db.Column(db.Date, nullable=False)
    time = db.Column(db.String, nullable=False)
    max_passengers = db.Column(db.Integer, nullable=False)
    num_passengers = db.Column(db.Integer, nullable=False, default=0)
    willing_to_stop = db.Column(db.Boolean, nullable=False)
    trip_cost = db.Column(db.Integer, nullable=False)

    # User as Driver
    user_id = (db.Column(db.Integer,
                         db.ForeignKey('users.user_id'),
                         nullable=False))
    # Places
    origin = db.Column(db.String(64), nullable=False)
    destination = db.Column(db.String(64), nullable=False)
    distance_meters = db.Column(db.Integer, nullable=False)
    display_distance = db.Column(db.String(15), nullable=False)

    # Back reference to User
    user = (db.relationship("User",
                            backref=db.backref("trips",
                                               order_by=trip_id)))

    def to_json(self):  # pragma: no cover
        """Serialize data."""
        datetime_str = self.date_of_trip.strftime('%Y-%m-%d')

        return {'tripId': self.trip_id,
                'dateOfTrip': datetime_str,
                'maxPassengers': self.max_passengers,
                'numPassengers': self.num_passengers,
                'willingToStop': self.willing_to_stop,
                'tripCost': self.trip_cost,
                'origin': self.origin,
                'time': self.time,
                'destination': self.destination,
                'distanceMeters': self.distance_meters,
                'displayDistance': self.display_distance,
                'userAsDriver': self.user_id,
                'userFirstName': self.user.fname,
                'userProfileImg': self.user.user_profile_img}


class UserTrip(db.Model):  # pragma: no cover
    """User (passenger) has joined a trip."""

    __tablename__ = "user_trips"

    user_trip_id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    # Back reference to Trip
    trip_id = (db.Column(db.Integer,
                         db.ForeignKey('trips.trip_id'),
                         nullable=False))
    trip = (db.relationship("Trip",
                            backref=db.backref("user_trips",
                                               order_by=user_trip_id)))
    # User as Passenger
    user_id = (db.Column(db.Integer,
                         db.ForeignKey('users.user_id'),
                         nullable=False))
    # Back reference to User
    user = (db.relationship("User",
                            backref=db.backref("user_trips",
                                               order_by=user_trip_id)))

    def to_json(self):  # pragma: no cover
        """Serialize data."""
        datetime_str = self.trip.date_of_trip.strftime('%Y-%m-%d')

        return {'userTripId': self.user_trip_id,
                'tripId': self.trip_id,
                'userId': self.user_id,
                'dateOfTrip': datetime_str,
                'userFirstName': self.user.fname,
                'userProfileImg': self.user.user_profile_img,
                'userBio': self.user.user_bio,
                'origin': self.trip.origin,
                'time': self.trip.time,
                'destination': self.trip.destination,
                'displayDistance': self.trip.display_distance,
                'distanceMeters': self.trip.distance_meters,
                'numPassengers': self.trip.num_passengers,
                'driverFirstName': self.trip.user.fname,
                'driverProfileImg': self.trip.user.user_profile_img,
                'driverBio': self.trip.user.user_bio}

##############################################################################
# Helper functions


def connect_to_db(app, db_uri="postgresql:///rideshares"):  # pragma: no cover
    """Connect the database to our Flask app."""
    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


def example_data():  # pragma: no cover
    """Provide example data for tests.py."""
    b = "fakepw"
    hashed_pw = bcrypt.hashpw(b.encode("utf-8"), bcrypt.gensalt())

    user = User(fname="Jo",
                lname="Bama",
                email="jo@bama.com",
                user_bio="Friendly person",
                user_gender="Female",
                password=hashed_pw.decode("utf-8"),
                user_profile_img=("https://robohash.org/enimsolutaqui.png?size"
                                  "=50x50&set=set1"),
                user_social_media="twitter.com")

    db.session.add(user)

    trip = Trip(date_of_trip="11-13-2018",
                max_passengers="3",
                num_passengers="1",
                willing_to_stop=False,
                trip_cost="10",
                user_id="1",
                origin="San Francisco",
                destination="Los Angeles",
                distance_meters="15422",
                display_distance="13 mi")

    db.session.add(trip)
    db.session.commit()

if __name__ == "__main__":  # pragma: no cover
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")
