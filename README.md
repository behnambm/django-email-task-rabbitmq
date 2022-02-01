# django-email-task-rabbitmq
After a user signs up, send an email using a worker instance that receives messages from RabbitMQ

It takes a lot of time to send emails during the request/response cycle, so I'm using `RabbitMQ` to publish a task and receive the task using a worker instance. Using this method, the client will not wait for SMTP to complete.

### Run locally 

- Make sure you have RabbitMQ running on localhost(or change the `host` in `consumer.py` and `producer.py`)
- Install requirements. `pip install requirements.txt`
- Rename `.env.sample` file to `.env` and fill the required variables with proper data.
- Run django app. `python manage.py runserver`
- Run worker instance(consumer).  `python consumer.py`


Here is the diagram for better understanding.
![diagram](https://user-images.githubusercontent.com/26994700/151976631-c5837369-e591-4330-ae29-8b99ed2aed12.png)


