I used the Linode service to create a server that would at first run this 
application locally (using the IP address of the server). Eventually, when incorporating
Nginx, Gunicorn, Certbot, and Namecheap the application is able to be securley hosted online.

When working on this project, I created a python virutal environment that contains
all of the installed packages neccessary for this project, which are stored in the 
'requirements.txt' file. 

The data for this application were the news items from the Hacker News Portal, which
were handled with JSON formatting. JSON formatting allows for better readability.
Additionally, a database stored the new items data along with the authenticated users.
I used Python's SQLAlchelmy, which is similar to SQL, which is used for database management.

Nginx works with the static files of the project, whereas Gunicorn handles the rest
of the files. The client, which is the linode server, sends a request Nginx, and then 
to Gunicorn. Gunicon processes the request, sends it to Nginx and then it is sent back
to the client. 

Configure the following files:
/etc/ngnix/sites-enabled/flaskblog
/etc/supervisor/conf.d/flaskblog.conf
/etc/nginx/nginx.conf

In order for the website to update the new items every hour, I used crontab to 
create the cron job of updating or running the file the pulls the API data every 
hour. 

The domain name 'www.gphackernews.me' was bought by on Namecheap.com. Certbot provided
the instructions that would eventually allow my domain to be secured. The domain was connected
to the server and then before you know it, the web application is hosted on the web.
