A little document outlining how to create a database using postgres running locally.

# Launch Postgres

# Connect to Postgres as user 'postgres'
```psql -U postgres```

# Create a database, called 'should_i_buy_it'
```CREATE DATABASE should_i_buy_it;```

# Connect to the newly created db
psql -U postgres -d should_i_buy_it

# Create tables using ```create_database.sql```


