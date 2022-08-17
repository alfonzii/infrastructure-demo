from flask import Flask, render_template, flash, request
from wtforms import Form, validators, StringField, IntegerField, SubmitField
from time import sleep
import socket
import sys, logging
import random

# Serialization/deserialization tool
import pickle



# App config.
app = Flask(__name__)
#app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

# Uncomment this to enable debugging prints
#logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


host = socket.gethostname()
ipaddr = socket.gethostbyname(host)


def send(key: str, value: int):
    clientSocket = socket.socket()
    db_hostname = "db"
    port = 25000
    
    connected = False
    
    logging.debug('Trying to connect to db')
    while not connected:
        try:
            clientSocket.connect( ( db_hostname, port ) )
            connected = True
        except socket.error:
            num = (random.random()) * 10
            sleep(num)
    logging.debug('Successfully connected. Now trying to send data.') 
    
    while True:
        try:
            clientSocket.send( pickle.dumps((key, value)) )

        except socket.error:
            # set connection status and recreate socket
            connected = False
            clientSocket = socket.socket()
            logging.debug('Connection lost... reconnecting') 
            while not connected:
                # attempt to reconnect, otherwise sleep for 2 seconds
                try:
                    clientSocket.connect( ( db_hostname, port ) )
                    connected = True
                    logging.debug( "re-connection successful" )
                except socket.error:
                    num = (random.random()) * 10
                    sleep( num )
        
        logging.debug("Successfully sent.")
        break
    clientSocket.close()


class ReusableForm(Form):
    name = StringField('Name: ', validators=[validators.InputRequired()])
    quantity = IntegerField('Quantity [1-25]: ', validators=[validators.NumberRange(min=1, max=25), validators.InputRequired()])
    
    @app.route("/", methods=['GET', 'POST'])
    def hello():
        form = ReusableForm(request.form)
    
        print (form.errors)
        if request.method == 'POST':
            name=request.form['name']
            quantity=request.form['quantity']
            print (name)
    
        if form.validate():
            logging.debug('Sending...')
            send(name, quantity)
            
            flash('Hello ' + name + ' with quantity ' + quantity)
            flash('From hostname \"' + host + '\" with IP: ' + ipaddr)
        else:
            flash('Hello from hostname \"' + host + '\" with IP ' + ipaddr)

        form.name.data = ""
        return render_template('hello.html', form=form)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
