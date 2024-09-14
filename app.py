from flask import Flask, request, jsonify
from instagrapi import Client
from instagrapi.exceptions import LoginRequired
import dearpygui.dearpygui as dpg
import threading
import requests
import json
import random

################################ Const ################################
teams = [
    'DS PENSKE', 'Jaguar TCS Racing', 'MAHINDRA RACING', 'Envision Racing',
    'Nissan Formula E Team', 'Nissan Formula E Team', 'Avalanche Andretti Formula E',
    'NIO 333 Racing FE Team', 'Envision Racing', 'Maserati MSG Racing', 'NEOM McLaren Formula E Team',
    'ABT CUPRA FORMULA E TEAM', 'MAHINDRA RACING', 'Jaguar TCS Racing', 'TAG Heuer Porsche Formula E Team'
]


def simul_racers_data(teams):
    names = [
        "Jake Dennis", "Stoffel Vandoorne", "Sergio Camara", "Robin Frijns",
        "Jake Hughes", "Maximilian Gunther", "Sam Bird", "Mitch Evans",
        "Lucas di Grassi", "Antonio Felix da Costa", "Sébastien Buemi",
        "Norman Nato", "Jehan Daruvala", "Nyck de Vries", "Oliver Rowland",
        "Sacha Fenestraz", "Jean-Eric Vergne", "Dan Ticktum", "Nick Cassidy",
        "Edoardo Mortara", "Nico Müller", "Pascal Wehrlein"
    ]

    racers_data = [
        {
            "name": name.lower().replace(" ", "-"),
            "team": random.choice(teams).lower().replace(" ", "-"),
            "points": [random.randint(0, 100) for _ in range(17)]
        }
        for name in names
    ]

    return racers_data


def force_question(field, values):
    resp = ""
    while resp not in values:
        print(f"Invalid {field}")
        for i in values:
            print(f"- {i}")
        resp = input(f"{field}: ")
    return resp


racers_data = simul_racers_data(teams)

app = Flask(__name__)


def run_flask():
    app.run(debug=True, use_reloader=False)


################################ Corredores ################################

def racer(racer_name):
    for racer in racers_data:
        if racer["name"] == racer_name.lower().replace(" ", "-"):
            return racer


def all_racers():
    return [racer for racer in racers_data]


def top_racer():
    top_racers = []
    max_points = 0

    for racer in racers_data:

        total_points = sum(racer["points"])
        if total_points > max_points:
            top_racers = [racer]
            max_points = total_points

        elif total_points == max_points:
            top_racers.append(racer)

    return {"racers": top_racers}


def total_points(field, var):
    if field == "" or var == "":
        raise ValueError("Field or variable not informed")

    total = 0
    for racer in racers_data:
        if racer[field] == var.lower().replace(" ", "-"):
            total += sum(racer["points"])

    return {
        field: var.lower().replace(" ", "-"),
        "total": total
    }


def team_racers(team):
    return [racer for racer in racers_data if racer["team"] == team.lower().replace(" ", "-")]


def all_teams():

    return [{team: team_racers(team)} for team in teams]


################################ Instagram ################################

def conn_instagram(data):
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        raise ValueError("Username and password are required")

    cl = Client()
    cl.login(username, password)
    return cl


################################ API ################################

@app.route('/racer', methods=['GET'])
def get_racer():
    try:
        racer_name = request.args.get("name")
        return jsonify(racer(racer_name)), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500


@app.route('/racers', methods=['GET'])
def get_all_racers():
    try:
        return jsonify(all_racers()), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500


@app.route('/team', methods=['GET'])
def get_team_racers():
    try:
        field = request.args.get('team')

        return jsonify(team_racers(field)), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500


@app.route('/teams', methods=['GET'])
def get_all_teams_racers():
    try:
        return jsonify(all_teams()), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500


@app.route('/top', methods=['GET'])
def top_racer_info():
    try:
        return jsonify(top_racer()), 200

    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500


@app.route('/points', methods=['GET'])
def get_total_points():
    try:
        field = request.args.get('field')
        var = request.args.get('var')

        return jsonify(total_points(field, var)), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500


@app.route('/connect', methods=['POST'])
def connect_instagram():
    try:
        client = conn_instagram(request.json)
        user_id = client.user_id_from_username(client.username)

        if not user_id:
            return jsonify({"error": "Failed to retrieve user ID"}), 400

        return jsonify({"coins": 1000}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except LoginRequired:
        return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500


def top(sender, data):
    try:

        response = requests.get("http://127.0.0.1:5000/top")
        if response.status_code == 200:
            print("Data successfully sent to Flask.")

            response_obj = json.loads(response.text)
            response_str = json.dumps(response_obj, indent=2)
            print(response_str)  # Mostra os dados retornados pelo Flask
        else:
            print("Failed to send data.")
    except Exception as e:
        print(f"Error sending data: {e}")
def name(sender, data):
    try:
        response = requests.get("http://127.0.0.1:5000/points?field=name&var=norman-nato")
        if response.status_code == 200:
            print("Data successfully sent to Flask.")
            response_obj = json.loads(response.text)
            response_str = json.dumps(response_obj, indent=2)
            print(response_str)  # Mostra os dados retornados pelo Flask
        else:
            print("Failed to send data.")
    except Exception as e:
        print(f"Error sending data: {e}")
def teams_pont(sender, data):
    try:
        response = requests.get("http://127.0.0.1:5000/points?field=team&var=avalanche-andretti")
        if response.status_code == 200:
            print("Data successfully sent to Flask.")
            response_obj = json.loads(response.text)
            response_str = json.dumps(response_obj, indent=2)
            print(response_str)  # Mostra os dados retornados pelo Flask
        else:
            print("Failed to send data.")
    except Exception as e:
        print(f"Error sending data: {e}")

def teams_all(sender, data):
    try:
        response = requests.get("http://127.0.0.1:5000/teams")
        if response.status_code == 200:
            print("Data successfully sent to Flask.")
            response_obj = json.loads(response.text)
            response_str = json.dumps(response_obj, indent=2)
            print(response_str)  # Mostra os dados retornados pelo Flask
        else:
            print("Failed to send data.")
    except Exception as e:
        print(f"Error sending data: {e}")

def teams_ind(sender, data):
    try:
        response = requests.get("http://127.0.0.1:5000/team?team=Jaguar TCS Racing")
        if response.status_code == 200:
            print("Data successfully sent to Flask.")
            response_obj = json.loads(response.text)
            response_str = json.dumps(response_obj, indent=2)
            print(response_str)  # Mostra os dados retornados pelo Flask
        else:
            print("Failed to send data.")
    except Exception as e:
        print(f"Error sending data: {e}")

def racer_all(sender, data):
    try:
        response = requests.get("http://127.0.0.1:5000/racers")
        if response.status_code == 200:
            print("Data successfully sent to Flask.")
            response_obj = json.loads(response.text)
            response_str = json.dumps(response_obj, indent=2)
            print(response_str)  # Mostra os dados retornados pelo Flask
        else:
            print("Failed to send data.")
    except Exception as e:
        print(f"Error sending data: {e}")

def racer_ind(sender, data):
    try:
        response = requests.get("http://127.0.0.1:5000/racer?name=norman-nato")
        if response.status_code == 200:
            print("Data successfully sent to Flask.")
            response_obj = json.loads(response.text)
            response_str = json.dumps(response_obj, indent=2)
            print(response_str)  # Mostra os dados retornados pelo Flask
        else:
            print("Failed to send data.")
    except Exception as e:
        print(f"Error sending data: {e}")
def start_flask(sender, data):
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True  # Permite que o Flask pare junto com o programa principal
    flask_thread.start()

def prnt():
    print(all_teams())
# Função para criar a janela no DearPyGui
def create_window():
    dpg.create_context()

    with dpg.window(label="Main Window", width=600, height=300):
        dpg.add_button(label="top", callback=top)
        dpg.add_button(label="name", callback=name)
        dpg.add_button(label="team_ponto", callback=teams_pont)
        dpg.add_button(label="teams", callback=teams_all)
        dpg.add_button(label="team", callback=teams_ind)
        dpg.add_button(label="Corredores", callback=racer_all)
        dpg.add_button(label="Corredor", callback=racer_ind)
        dpg.add_button(label="print", callback=prnt)
        # dpg.add_button(label="Send Data to Flask", callback=top)

    dpg.create_viewport(title='DearPyGui & Flask Communication', width=600, height=300)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    # Iniciar o servidor Flask em uma thread separada
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True  # Garantir que o Flask pare quando o programa fechar
    flask_thread.start()

    # Iniciar a interface DearPyGui
    create_window()
# Iniciar a interface do DearPyGui