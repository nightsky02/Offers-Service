# Simple service for storage  offers
This service processes excel files with information about offers and storage them in the local database. Using special endpoints, it allows to send a file with offers, and get basic information about storaged offers with filters.

## Installation
1. Clone the repository using `git clone`
2. Make a virtual environment in the repository folder, using `python -m venv .venv`
3. Install the necessary dependencies:
   ```python
   pip install "fastapi[standard]" sqlalchemy  mysql-connector-python openpyxl
   ```
4. Set the environment variable DB_URL with your MySQL database url
5. Restart your terminal or IDE (if you have opened project in IDE)
   

## Usage
- Run the application using the command `python -m app.main` (by default, the server runs on the 8000 port)
### File uploading
- Go to `http://localhost:8000/docs`, open the `upload` endpoint, write any user id and upload your excel file (the file structure described in the next section) or use the default templates from the repository folder
- The result will be a html page that shows the offers which have/haven't passed the validation, and the simple statistics (more informative statistics is printed in the terminal):
  - The updated count
  - The deleted count
  - The offers which really have been pushed in the database
### Checking offers
- Go to http://localhost:8000/offers. You can also open this endpoint in the `/docs` page, but directly is much more beautiful.
- Use the following query parameters to filter your results. You can also combine them:
  - **seller_id** - specify the seller id
  - **offer_id** - specify the offer id
  - **substr** - specify some piece of string which will be used for finding offers by their title
- Examples:
  
  - `seller_id=3&offer_id=4` -> get the 4th offer from the 3th seller
  - `substr=mouse` -> get all offers which contains `mouse` in their name
  - `seller_id=4&substr=mouse` -> get offers from 4th seller, which contains `mouse`
  
## Excel file structure
By default, each excel file must contain ONLY 5 cells in one row:
1. offer_id - the id of the offer. Cannot be empty or negative.
2. name - the title of the offer. Valid if length >=1.
3. price - the price of the offer. Can be seperated by comma or dot
4. quantity. Must be >= 0.
5. avaivable - boolean value (0, or 1). If is set to 0, it will be deleted from database, or it will not be pushed in the database.

The first row of the document is considered as a "title row" - the row which contains titles of the cells (check the templates)
### Default excel file templates
There are three excel files in the repository folder, which help to look at how the service behaves with different data:
- data_duplicated - contains two offers with the same offer id. 
- data_long - contains 99 different offers
- data_with_empty-name - contains one offer with empty name.