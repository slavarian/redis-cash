# Сервис для поиска самых дешёвых отелей
# через сторонние сервисы

import redis
import time
import flask
import services
from booking import Booking, Hotel
import datetime

r = redis.Redis(host='localhost',
                port=6379, decode_responses=True)

app = flask.Flask(__name__)
booking = Booking(
    datetime.datetime(2023, 5, 1),
    datetime.datetime(2023, 5, 7)
)


@app.route('/')
def main_page():
    redis_cash:list[Hotel] = []
    hotels: list[Hotel] = booking.get_info()
    for i in range(len(hotels)):
        h = r.get(f"hotels{i}")
        p = r.get(f"price{i}")
        redis_list:list = Hotel(name=h, price=p)
        redis_cash.append(redis_list)
    return flask.render_template('index.html', hotels=hotels, redis_cash=redis_cash)


hotels: list[Hotel] = booking.get_info()
for i,b in enumerate(hotels):
    r.set(f"hotels{i}", b.name)
    r.set(f"price{i}", b.price)
    # print(b.name)




if __name__ == '__main__':
    app.run(host="localhost",
            port=8090,
            debug=True)
