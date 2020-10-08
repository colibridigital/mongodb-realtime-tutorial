import requests
import pymongo
import os
import argparse


def write_to_mongo(resp_parsed):
    # Establish connection with MongoDB Atlas
    atlasdb_connection_string = "mongodb+srv://sandbox.nupbd.mongodb.net"
    mongo_username = os.environ['MONGODB_USERNAME']
    mongo_password = os.environ['MONGODB_PASSWORD']

    try:
        client = pymongo.MongoClient(
            atlasdb_connection_string,
            username=mongo_username,
            password=mongo_password)
        # Insert parsed response
        db = client.sandbox
        db.uspopulation.insert_many(resp_parsed)
    except Exception as e:
        print(e)
    finally:
        client.close()


def parse_api_call(year):
    # Make API request to US Census API
    api_code = os.environ['API_CODE']
    # https://api.census.gov/data/2018/acs/acs1/variables.html
    acs_req = "https://api.census.gov/data/{0}/acs/acs1?get=NAME,B01001_001E,B01001_002E,B01001_026E&for=metropolitan%20statistical%20area/micropolitan%20statistical%20area&key={1}".format(
        year, api_code)

    r = requests.get(acs_req)

    # Adjust Response
    resp_parsed = []
    for row in r.json():
        if row[0] == 'NAME':
            continue
        resp_parsed.append(
            {
                'year': year,
                'statistical_area_id': row[4],
                'statistical_area_name': row[0],
                'statistical_area_state': row[0].split(",")[1].lstrip(),
                'details':
                {
                    'total_population': int(row[1]),
                    'total_population_male': int(row[2]),
                    'total_population_female': int(row[3])
                }
            }
        )

    return resp_parsed


def main():
    parser = argparse.ArgumentParser(description='This is a MongoDB Tutorial')

    parser.add_argument('--year', action='store', dest='year',
                        help='Should be a year(2005-2018)')
    parser.add_argument('--mongo', action='store', dest='mongo',
                        help='Should be a boolean')

    year = parser.parse_args().year
    mongo = parser.parse_args().mongo

    print("Year is " + year)

    resp_parsed = parse_api_call(year)

    if mongo == 'y':
        write_to_mongo(resp_parsed)
    else:
        print(resp_parsed)


if __name__ == '__main__':

    main()
