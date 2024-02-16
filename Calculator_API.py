import sys
from urllib.parse import unquote
from flask import Flask, jsonify, request

app = Flask(__name__)


####################
## Calculator API ##
####################

class Calcul:
    id = -1
    operand1 = 1
    operator = ""
    operand2 = 1

    def __init__(self, id, operand1, operator, operand2):
        Calcul.id += 1
        self.operand1 = operand1
        self.operator = operator
        self.operand2 = operand2
    
    def calculate(self):
        if self.operator == "+":
            return self.operand1 + self.operand2
        elif self.operator == "-":
            return self.operand1 - self.operand2
        elif self.operator == "*":
            return self.operand1 * self.operand2
        elif self.operator == "/":
            if self.operand2 != 0:
                return self.operand1 / self.operand2
            else:
                return "Error : Division by 0 impossible..."
        else:
            return "Error : Invalid operator"

"""
test_calcul = Calcul(Calcul.id, 1, "+", 1)

operations = {}
result = test_calcul.operand1
operations[str(test_calcul.id)] = (test_calcul.operand1, test_calcul.operator, test_calcul.operand2, test_calcul.calculate())
"""

def value(x):
    return unquote(unquote(x))

@app.route('/')
def main_menu():
    current_url = request.headers.get('X-Forwarded-Proto', 'http') + '://' + request.headers.get('X-Forwarded-Host', 'localhost')
    if current_url.endswith('/'):
        current_url = current_url[:-1]
    text = "<h2 style = 'text-align : center;'>To use the calculator, please type in the first operand, then the operator (\"+\", \"-\", \"*\", or \"%2F\" for division), then the second operand.</h2><br>"
    
    return text

"""

@app.route('/viewCalculs', methods = ["GET"])
def viewCalculs():
    return jsonify(operations)


@app.route('/calculate/<operand1>/<operator>/<operand2>', methods = ["GET", "POST"])
def calculate(operand1, operator, operand2):
    new_calcul = Calcul(Calcul.id, int(operand1), value(operator), int(operand2))
    operations[str(new_calcul.id)] = (int(new_calcul.operand1), value(new_calcul.operator), int(new_calcul.operand2), new_calcul.calculate())
    return str(new_calcul.id)


@app.route('/viewCalculWithId/<id>', methods = ["GET"])
def viewCalculWithId(id):
    return jsonify(operations[str(id)])

"""

########################
## Storage with Redis ##
########################
import redis
from redis_dict import RedisDict

r = redis.Redis(host='localhost', port=6379, db=0)
operations = RedisDict()

test_calcul = Calcul(Calcul.id, 1, "+", 1)

result = test_calcul.operand1
operations[str(test_calcul.id)] = (test_calcul.operand1, test_calcul.operator, test_calcul.operand2, test_calcul.calculate())

@app.route('/viewCalculs', methods = ["GET"])
def viewCalculs():
    return jsonify(dict(operations))

"""
@app.route('/calculate/<operand1>/<operator>/<operand2>', methods = ["GET", "POST"])
def calculate(operand1, operator, operand2):
    new_calcul = Calcul(Calcul.id, int(operand1), value(operator), int(operand2))
    operations[str(new_calcul.id)] = (int(new_calcul.operand1), value(new_calcul.operator), int(new_calcul.operand2), new_calcul.calculate())
    return str(new_calcul.id)
"""


@app.route('/viewCalculWithId/<id>', methods = ["GET"])
def viewCalculWithId(id):
    return jsonify(dict(operations[str(id)]))


##########################
## Queues with RabbitMQ ##
##########################
import pika

@app.route('/calculate/<operand1>/<operator>/<operand2>', methods = ["GET", "POST"])
def calculate(operand1, operator, operand2):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='calculs')

    new_calcul = Calcul(Calcul.id, int(operand1), value(operator), int(operand2))
    operations[str(new_calcul.id)] = (int(new_calcul.operand1), value(new_calcul.operator), int(new_calcul.operand2), new_calcul.calculate())

    channel.basic_publish(exchange='', routing_key='calculs', body=(str(new_calcul.id), jsonify(dict(operations[str(new_calcul.id)]))))
    print(" [x] Sent a calcul with its id.")
    connection.close()



if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "check_syntax":
            print("Build OK")
            exit(0)
        else:
            print("Passed argument not supported ! Supported arguments : check_syntax")
            exit(1)

    app.run(debug = True)