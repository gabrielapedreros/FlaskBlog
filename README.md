# Flask Blog
I used the Linode service to create a server that would at first run this 
application locally (using the IP address of the server). Eventually, when incorporating
Nginx, Gunicorn, Certbot, and Namecheap the application is able to be securley hosted online.

# Python Virutal Environment 
When working on this project, I created a python virutal environment that contains
all of the installed packages neccessary for this project, which are stored in the 
'requirements.txt' file. 

# Hacker News Portal API
The data for this application were the news items from the Hacker News Portal, which
were handled with JSON formatting. JSON formatting allows for better readability.
Additionally, a database stored the new items data along with the authenticated users.
I used Python's SQLAlchelmy, which is similar to SQL, which is used for database management.

# Web Application Server Deployment 
Nginx works with the static files of the project, whereas Gunicorn handles the rest
of the files. The client, which is the linode server, sends a request Nginx, and then 
to Gunicorn. Gunicon processes the request, sends it to Nginx and then it is sent back
to the client. 

# Configuration 
Configure the following files:
/etc/ngnix/sites-enabled/flaskblog
/etc/supervisor/conf.d/flaskblog.conf
/etc/nginx/nginx.conf

# Cron Job - Update News Items Hourly
In order for the website to update the new items every hour, I used crontab to 
create the cron job of updating or running the file the pulls the API data every 
hour. 

# Domain and HTTPS
The domain name 'www.gphackernews.me' was bought by on Namecheap.com. Certbot provided
the instructions that would eventually allow my domain to be secured. The domain was connected
to the server and then before you know it, the web application is hosted on the web.

# Unit Test Coverage
Name                      Stmts   Miss  Cover
---------------------------------------------
flaskblog/__init__.py        30      3    90%
flaskblog/extensions.py       4      0   100%
flaskblog/forms.py            6      0   100%
flaskblog/hackernews.py      14      1    93%
flaskblog/models.py          30      3    90%
flaskblog/routes.py         103     57    45%
tests/test_models.py         34      0   100%
tests/test_routes.py         20      0   100%
---------------------------------------------
TOTAL                       241     64    73%

# Unit test, pipeline, CD/CI, 
