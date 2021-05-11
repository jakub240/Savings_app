This is an educational project of an app designed to help with managing savings and expenses.
More info below:

Manual:\
initialize model Cities and Category with  
python manage.py loaddata data_category.json\
python manage.py loaddata data_cities.json \

- migrate data
- run server

1. Try to log in.
2. If you don't have an account Create a profile
3. Go to "list of expenses"
4. Enjoy

Update 11.05.2021
- added pagination on expenses list on the main page

About:
The main view of an app ("Expenses") consists of expenses added by user. You can also add budgets for each category
(specify amount and period) and the site calculates (based on current expenses) how much money you can spend daily
to maintain the budget for selected period of time.

- app still is and will be developed in the future
- for now both Cities and Categories are limited to a couple of rows.
- since the course was focused on back-end functionalities, front-end side of the site is (for now) simplified (using no-style css in a form of a link in the base.html template).

