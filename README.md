# Warehouse Management - Backend

To run this server, just run `docker-compose up`, after adding the files `backend.env` and `mongo.env` as shown in the relevant examples. Remember to modify the values from the example to the appropriate ones. The server will then be accessible through [localhost](http://localhost).

Check the documentation for each route in the module docstring in the [views](./warehouse/views).


To modify the frontend to work with this server, any calls to Firestore should be modified to be `fetch` requests to the location where this server is hosted. Also, calls that modify the product quantity directly in the database should be modified to use the `change_quantity` endpoint.
