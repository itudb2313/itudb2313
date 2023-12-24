# ITU-BLG317E-DATABASE-SYSTEMS-PROJECT

CRN:12166

## GROUP MEMBERS

- Onur Baylam(onurbayl) - 150220770
- Orhan Berkay Yılmaz(orhosko) - 150210054
- Muhammed Necati Polat(MuhammedNecatiPolat) - 070200734
- Murat Arda Saracoglu(ardasarac44) - 150210704	
- Mustafa Taha Pamuk(Undreamid)- 150200703

## Introduction

All-in-one system for car retailers.

## Quick Start

1. Clone the repository:

        git clone https://github.com/itudb2313/itudb2313
        cd itudb2313

2. Initialize and activate a virtual environment:

        python3 -m venv .venv
        source .venv/bin/activate
        (.venv\Scripts\active for Windows)

3. Install the dependencies:

        pip install -r requirements.txt

4. Create config.py file with these inside:

        DB_HOST = "localhost"
        DB_USER = "root"
        DB_PASSWORD = "******"
        DB_DATABASE = "test"

        PORT = 8080
        DEBUG = True

5. Run the development server:

        flask run

## Features

List the key features of your project:

- Feature 1
- Feature 2
- Feature 3
