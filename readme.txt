1. To get the code either download directly from https://github.com/jmpdevelopment/Suade-home-task or run 'git clone https://github.com/jmpdevelopment/Suade-home-task.git' from Git terminal
2. Once downloaded navigate to code top level repository and run 'pip install -r requirements.txt' - to install all required packages
3. Run 'pip install -e .' to install app package (for tests to work properly)
4. Data for application and test data is already prepared and loaded into app/orders_data.db and tests/test.db respectively
5. If you need to reload raw data provided you can run initialize_data.py script directly for main application data (you will need to delete orders_data.db from app directory first)
6. To reload test data:
    a. Delete current test.db ir tests directory
    b. Start Python shell in code root folder
    c. run 'from initialize_data import initialize_data, test_db_path, test_data_source_path'
    d. run 'initialize_data(test_db_path, test_data_source_path)'
    e. Close python shell and check if test.db was created in tests directory
7. To run application itself just run 'run.py' module
8. Once application is running open your browser and go to 'http://127.0.0.1:5000/api/v1/orders_data_by_date?date=20190801' for example query
9. To run tests either run test_app.py in tests directory directly or run pytest at root folder


Example API usage:
    Terminal: curl http://127.0.0.1:5000/api/v1/orders_data_by_date?date=20190801  
    Browser: http://127.0.0.1:5000/api/v1/orders_data_by_date?date=20190801

Note that date must be provided in yyyymmdd format

Example response:

{
  "commissions": {
    "order_average": 1008.22, 
    "promotions": {
      "1": 0, 
      "2": 188049.4, 
      "3": 0, 
      "4": 0, 
      "5": 409117.8
    }, 
    "total": 9073.99
  }, 
  "customers": 9, 
  "discount_rate_avg": 0.13, 
  "items": 2895, 
  "order_total_avg": 1182286.1, 
  "total_discount_amount": 130429980.26
}