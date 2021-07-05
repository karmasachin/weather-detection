import requests
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost/weather"

db = SQLAlchemy(app)

class Detail(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        new_city = request.form.get('city')
        
        if new_city:
            new_city_obj = Detail(city=new_city)

            db.session.add(new_city_obj)
            db.session.commit()

    cities = Detail.query.all()
    cities= cities[len(cities)-2:len(cities)]
    print(len(cities))
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=271d1234d3f497eed5b1d80a07b3fcd1'

    weather_data = []

    for cit in cities:
        print(cit.city)
        r = requests.get(url.format(cit.city)).json()
        print(r)
        print(r['clouds']['all'])
        weather = {
            'city' : cit.city,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }

        weather_data.append(weather)


    return render_template('weather.html', weather_data=weather_data)


if(__name__=="__main__"):
    app.run(debug= True)