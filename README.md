# FlaskWatchdog
<p>FlaskWatchdog is a website monitoring tool built with Flask, Celery, and SQLAlchemy. It allows users to add websites they want to monitor and receive email notifications when a website goes down or comes back online. The application also features rate limiting, logging, and user authentication with different levels of privileges.</p>

        ┌───────────┐         ┌───────────────┐
        │   User    │         │     Redis     │
        └───────────┘         └───────────────┘
              │                       ▲
              │                       │
              ▼                       │
        ┌───────────┐                 │
        │UserWebsite│     ┌───────────┐
        └───────────┘     │   Celery  │
              │           └───────────┘
              │                 │     
              ▼                 │     
        ┌───────────┐           │     
        │  Website  │◄──────────┘     
        └───────────┘                 
<ul><li>Users have a one-to-many relationship with UserWebsite objects</li><li>Websites have a many-to-many relationship with UserWebsite objects</li><li>Redis is used as a message broker to manage Celery tasks</li><li>Celery is used to periodically check the status of websites and send email notifications to users when a website goes offline or comes back online.</li></ul>
<h2>Requirements</h2>
<ul>
  <li>Python 3.7 or higher</li>
  <li>Redis</li>
  <li>SQLlite</li>
</ul>
<h2>Installation</h2>
<ol>
  <li>
    <p>Clone the repository:</p>
    <pre><code>git clone https://github.com/&lt;username&gt;/flask-watchdog.git
cd flask-watchdog</code></pre>
  </li>
  <li>
    <p>Create and activate a virtual environment:</p>
    <pre><code>python3 -m venv venv
source venv/bin/activate</code></pre>
  </li>
  <li>
    <p>Install the dependencies:</p>
    <pre><code>pip install -r requirements.txt</code></pre>
  </li>
  <li>
    <p>Set up the environment variables:</p>
    <pre><code>export SQLALCHEMY_DATABASE_URI=&lt;your-database-uri&gt;
export SECRET_KEY=&lt;your-secret-key&gt;
export MAIL_SERVER=&lt;your-mail-server&gt;
export MAIL_PORT=&lt;your-mail-port&gt;
export MAIL_USERNAME=&lt;your-mail-username&gt;
export MAIL_PASSWORD=&lt;your-mail-password&gt;
export CELERY_BROKER_URL=redis://localhost:6379/0
export CELERY_RESULT_BACKEND=redis://localhost:6379/0</code></pre>
  </li>
  <li>
    <p>Create the database:</p>
    <pre><code>flask db init
flask db migrate
flask db upgrade</code></pre>
  </li>
  <li>
    <p>Start the Flask application:</p>
    <pre><code>flask run</code></pre>
  </li>
  <li>
    <p>Start the redis server:</p>
    <pre><code>redis-server</code></pre>
  </li>
  <li>
    <p>Start the Celery worker:</p>
    <pre><code>celery -A app.celery celery -A app.celery worker --loglevel=INFO</code></pre>
  </li>
  <li>
    <p>Start the Celery beat scheduler:</p>
    <pre><code>celery -A app.celery celery -A app.celery beat --loglevel=INFO</code></pre>
  </li>
</ol>
<h2>Usage</h2>
<ol>
  <li>
    <p>Open your web browser and navigate to <code>http://localhost:5000</code>.</p>
  </li>
  <li>
    <p>Create an account by clicking on the "Register" link in the navigation bar.</p>
  </li>
  <li>
    <p>Log in with your email and password.</p>
  </li>
  <li>
    <p>Click on the "Add Website" button to add a website to monitor. Enter the URL of the website and click on the "Add Website" button.</p>
  </li>
 <li><p>The website will be added to your list of monitored websites. You will receive an email notification if the website goes down or comes back online.</p></li>
 <li><p>To delete a website from your list, click on the "Delete" button next to the website.</p></li>
 <li><p>To update your email address, click on the "Update Email" link in the navigation bar.</p></li>
 <li><p>To create an admin user, run the following command:</p><pre><span></span><code>flask create-admin <span>--email</span> &lt;admin-email&gt; <span>--password</span> &lt;admin-password&gt;
</code></pre></li>
  <li><p>To create a regular user, run the following command:</p><pre><span></span><code>flask <span>create</span><span>-</span><span>user</span> <span>--email &lt;user-email&gt; --password &lt;user-password&gt;</span>
</code></pre></li>
</ol>
<h2> Migration to PostgreSQL database</h2>
<p>To prepare your Flask app to use PostgreSQL database, you will need to follow these steps:</p>
<ol>
 <li><p>Install the <code>psycopg2</code> library by running the following command in your terminal:</p><pre><span></span>
 <code>pip install psycopg2-<span>binary</span>
</code></pre></li>
 <li><p>Update your <code>requirements.txt</code> file to include the <code>psycopg2-binary</code> library.</p></li>
 <li><p>Create a PostgreSQL database and user with appropriate permissions. You can do this using the <code>createdb</code> and <code>createuser</code> command-line utilities in PostgreSQL.</p></li>
 <li><p>Set the <code>SQLALCHEMY_DATABASE_URI</code> environment variable to the connection string for your PostgreSQL database. For example:</p><pre><span></span><code>postgresql://username:password@localhost/database_name
</code></pre><p>Replace <code>username</code> and <code>password</code> with your PostgreSQL username and password, respectively, and <code>database_name</code> with the name of your PostgreSQL database.</p></li>
 <li><p>Update your <code>config.py</code> file to use PostgreSQL as your database by setting the <code>SQLALCHEMY_DATABASE_URI</code> configuration variable to the value of the <code>SQLALCHEMY_DATABASE_URI</code> environment variable.</p></li>
 <li><p>In your <code>requirements.txt</code> file, add the <code>psycopg2-binary</code> library as a dependency.</p></li>
</ol>
<h2>Fields for improvement :</h2>
<ol>
 <li><p>Security: Although there are some security measures in place such as CSRF protection, password hashing, and rate limiting, there is still room for improvement. For example, implementing two-factor authentication, using secure cookies, and implementing strict access control policies can help improve the security of the application.</p></li>
 <li><p>Testing: There are currently no unit tests or integration tests for the application. Implementing automated tests can help ensure that the application is functioning correctly and can catch issues early in the development process.</p></li>
 <li><p>Error handling: The application has error handling for some HTTP error codes, but not all. Adding more comprehensive error handling can help improve the user experience and make it easier to diagnose issues.</p></li>
 <li><p>Scalability: The current implementation may not be scalable for a large number of users and websites. Implementing techniques such as load balancing, horizontal scaling, and caching can help improve the scalability of the application.</p></li>
 <li><p>Code structure: The current codebase could be refactored to make it more modular and easier to maintain. This could involve breaking up the code into smaller functions or classes, reducing the number of global variables, and improving code readability.</p></li>
</ol>
 
