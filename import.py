import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


def main():
    # opens file with CSV reader
    f = open("zips.csv")
    reader = csv.reader(f)

    # Skips header of CSV file
    next(reader, None)

    # loop through rows of CSV file
    for row in reader:

        # adds row to database
        db.execute("INSERT INTO locations(zipcode, city, state, lat, long, population) \
        VALUES(:zipcode, :city, :state, :lat, :long, :population)", {
                   "zipcode": row[0], "city": row[1], "state": row[2],
                   "lat": row[3], "long": row[4], "population": row[5]})

        # prints location information in the terminal
        print(f"{row[0]}, {row[1]}, {row[2]}, {row[3]}, {row[4]}, {row[5]}")

    # commit changes to database
    db.commit()


if __name__ == "__main__":
    main()
