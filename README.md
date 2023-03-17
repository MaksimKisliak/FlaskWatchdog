<h1>FlaskWatchDog</h1>
<p>FlaskWatchDog is a web application that allows users to monitor the status of their websites. Users can add websites to their dashboard, and the app will periodically check the status of these websites. Users will be notified when their website goes down or comes back online. The app is designed as a challenge to itself.</p>
<h2>Table of Contents</h2>
<ul>
<li><a>Installation</a></li>
<li><a>Usage</a></li>
<li><a>Admin Features</a></li>
<li><a>Maintaining the App</a></li>
<li><a>CLI commands</a></li>
<li><a>Testing</a></li>
<li><a>Deployment</a></li>
<li><a>Monitoring and Logging</a></li>
<li><a>Updating the App</a></li>
  <li><a>Contributing</a></li>
<li><a>Troubleshooting</a></li>
</ul>
<h2>Installation</h2>
<p>Follow these steps to install the app:</p>
<ol>
<li>Clone this repository:</li>
</ol>
<pre>
<code>git clone https://github.com/MaksimKisliak/FlaskWatchdog
</code>
</pre>
<p>2. Create a virtual environment and activate it:</p>
<pre>
<code>cd FlaskWatchDog
python3 -m venv venv
source venv/bin/activate
</code>
</pre>
<p>3. Install the required packages:</p>
<pre>
<code>pip install -r requirements.txt
</code>
</pre>
<p>4. Set up the environment variables:</p>
<pre>
<code>
FLASK_CONFIG="config.DevelopmentConfig"
FLASK_APP="run.py"
SECRET_KEY="klk@#fsdjfonj134njnf"
MAIL_PASSWORD="a2AxKKAGKxsTs28KMfzY"
MAIL_PORT="465"
MAIL_SERVER="smtp.mail.ru"
MAIL_USERNAME="makskislyak1@mail.ru"
CELERY_BROKER_URL="redis://localhost:6379/0"
DEV_DATABASE_URI="sqlite:///flaskwatchdog_dev.db"
TEST_DATABASE_URI="sqlite:///flaskwatchdog_test.db"
PROD_DATABASE_URI="sqlite:///flaskwatchdog_prod.db"
</code>
</pre>
<p>5. Initialize the database:</p>
<pre>
<code>flask db init
flask db migrate -m "Initial migration"
flask db upgrade
</code>
</pre>
<p>6. Start the development server:</p>
<pre>
<code>flask run
</code>
</pre>
<h2>Usage</h2>
<p>Follow these steps to use the app:</p>
<ol>
<li><p>Open your web browser and visit <code>http://localhost:5000/</code>.</p></li>
<li><p>Register a new account and log in to your dashboard.</p></li>
<li><p>Add websites you want to monitor by entering their URLs.</p></li>
<li><p>The app will periodically check the status of your websites and notify you when they go down or come back online.</p></li>
</ol>
<h2>Admin Features</h2>
<p>As an admin, you can:</p>
<ul>
<li>Add new users manually</li>
<li>View all users, websites, and user-website relationships</li>
</ul>
<p>To access the admin panel, visit <code>http://localhost:5000/admin</code>.</p>
<h2>Maintaining the App</h2>
<p>Follow these steps to maintain the app:</p>
<ol>
<li>Regularly update the packages:</li>
</ol>
<pre>
<code>pip install -U -r requirements.txt
</code>
</pre>
<p>2. Keep your repository up to date with the latest changes:</p>
<pre>
<code>git pull origin main
</code>
</pre>
<p>3. Periodically check for security vulnerabilities:</p>
<pre>
<code>pip install safety
safety check
</code>
</pre>
<p>4. Monitor the logs for any errors or issues:</p>
<pre>
<code>tail -f logs/app.log
</code>
</pre>
<p>5. Backup the database regularly:</p>
<pre>
<code>cp FlaskWatchDog.db backup/FlaskWatchDog.db_$(date +%Y-%m-%d_%H-%M-%S)
</code>
</pre>
<h2>CLI commands</h2>
<ol>
<li>
<p><strong>Activate your virtual environment</strong> (if you are using one):</p>
<pre><code>source venv/bin/activate</code></pre>
</li>
<li>
<p><strong>Set environment variables</strong>:</p>
<pre><code>export FLASK_APP=run.py</code></pre>
<pre><code>export FLASK_ENV=development</code></pre>
</li>
<li>
<p><strong>Run CLI commands</strong>:</p>
<p>To run the custom CLI command <code>check-status</code> in your Flask app, use the following command:</p>
<pre><code>flask check-status</code></pre>
</li>
<li>
<p><strong>Install and start Redis</strong>:</p>
<p>Install Redis, if not already installed:</p>
<pre><code>brew install redis</code></pre>
<p>Start Redis server:</p>
<pre><code>redis-server</code></pre>
<p>Check Redis connection by running the following command:</p>
<pre><code>redis-cli ping</code></pre>
<p>If the connection is successful, you will receive the "PONG" response.</p>
</li>
<li>
<p><strong>Run Celery worker and Celery beat</strong>:</p>
<p>Start Celery worker:</p>
<pre><code>celery -A run.celery worker --loglevel=INFO</code></pre>
<p>Start Celery beat:</p>
<pre><code>celery -A run.celery beat --loglevel=INFO</code></pre>
<p>Make sure to replace <code>run</code> with the name of your entry point file if it is different from <code>run.py</code>.</p>
</li>
</ol>
<h2>Testing</h2>
<p>Before deploying changes to production, run tests to ensure that everything works as expected.</p>
<ol>
<li>Install the testing requirements:</li>
</ol>
<pre><code>pip install -r requirements-test.txt</code></pre>
<ol start="2">
<li>Run the tests:</li>
</ol>
<pre><code>pytest</code></pre>
<ol start="3">
<li>Check the code coverage:</li>
</ol>
<pre><code>coverage run -m pytest
coverage report<p>app/__init__.py                            59      3    95%
app/auth/__init__.py                        4      0   100%
app/auth/routes.py                         97     39    60%
app/cli.py                                 91      9    90%
app/errors/__init__.py                      4      0   100%
app/errors/handlers.py                     13      4    69%
app/extensions.py                          17      0   100%
app/forms.py                               23      0   100%
app/main/__init__.py                        4      0   100%
app/main/routes.py                        105     34    68%
app/make_celery.py                          5      0   100%
app/models/user.py                         33      4    88%
app/models/userwebsite.py                  12      0   100%
app/models/website.py                      10      1    90%
config.py                                  35      1    97%
run.py                                     10      1    90%
test/__init__.py                            0      0   100%
test/conftest.py                           58      1    98%
test/functional/__init__.py                 0      0   100%
test/functional/test_commands.py           40      0   100%
test/integration/__init__.py                0      0   100%
test/integration/celery_redis_test.py      35      0   100%
test/integration/test_app.py               65      1    98%
-----------------------------------------------------------
TOTAL                                     720     98    86%
</p></code></pre>
<h2>Deployment</h2>
<ol>
<li>Set up the production environment variables:</li>
</ol>
<ol start="2">
<li>Install a production-ready WSGI server, such as Gunicorn:</li>
</ol>
<pre><code>pip install gunicorn</code></pre>
<ol start="3">
<li>Start the server:</li>
</ol>
<pre><code>gunicorn -w 4 -b 0.0.0.0:8000 run:app</code></pre>
<ol start="4">
<li><p>Set up a reverse proxy, such as Nginx, to forward requests to Gunicorn.</p></li>
<li><p>Configure SSL/TLS using a service like Let's Encrypt.</p></li>
<li><p>Set up periodic tasks for website monitoring using a task scheduler, such as Celery.</p></li>
</ol>
<h2>Monitoring and Logging</h2>
<ol>
<li><p>Monitor the application's performance using a monitoring tool, such as New Relic or Datadog.</p></li>
<li><p>Set up log rotation to manage log files and prevent them from consuming too much disk space.</p></li>
<li><p>Configure log aggregation and analysis using a service like Logstash, Elasticsearch, and Kibana (ELK Stack) or Graylog.</p></li>
<li><p>Set up alerts and notifications for critical events.</p></li>
</ol>
<h2>Updating the App</h2>
<ol>
<li>Pull the latest changes from the repository:</li>
</ol>
<pre>
<code>git pull origin <span>main</span>
</code>
</pre>
<ol start="2">
<li>Install any new dependencies:</li>
</ol>
<pre>
<code>pip install -r requirements.txt
</code>
</pre>
<ol start="3">
<li>Apply any new database migrations:</li>
</ol>
<pre>
<code>flask db upgrade
</code>
</pre>
<ol start="4">
<li>Restart the application server (e.g., Gunicorn) and reverse proxy (e.g., Nginx).</li>
</ol>
<h2>Troubleshooting</h2>
<p>If you encounter issues with the app, check the following:</p>
<ol>
<li><p>Review the logs for any error messages or stack traces.</p></li>
<li><p>Ensure that all required environment variables are set and have the correct values.</p></li>
<li><p>Verify that the database server is running and accessible.</p></li>
<li><p>Check the application server (e.g., Gunicorn) and reverse proxy (e.g., Nginx) configurations.</p></li>
<li><p>Confirm that all dependencies are installed and up-to-date.</p></li>
</ol>
<h2>Contributing</h2>
<p>If you want to contribute to this project, please follow these steps:</p>
<ol>
<li>Fork the repository.</li>
<li>Create a new branch with a descriptive name.</li>
<li>Make your changes and commit them to your branch.</li>
<li>Create a pull request and describe the changes you made.</li>
</ol>
<p>I will review your changes and decide whether to merge them into the main branch.</p>
<h2>License</h2>
<p>FlaskWatchDog is licensed under the MIT License. See the <a>LICENSE</a> file for more information.</p>

