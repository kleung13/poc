# poc

# Run the Application
Build the dockerfile
`docker run -dp 5000:5000 -w /app -v "$(pwd):/app" poc` Run it with an attached volume 

# Database

Set db_url or get the DATABASE_URL or else use local database sqlite:///data.db 

app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")  #sqllite Connection String

To set up the databse, use `flask db init`

`flask db migrate` will set up the tables

`flask db upgrade` will build the tables

## Connect to a CloudSQL DB

https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/cloud-sql/postgres/sqlalchemy

# Update Values

1. Blueprint
2. Schema
3. Table

