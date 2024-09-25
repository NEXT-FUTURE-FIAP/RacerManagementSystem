from flask import Flask, request, jsonify
from instagrapi import Client
from instagrapi.exceptions import LoginRequired
import dearpygui.dearpygui as dpg
import threading
import requests
import json
import random
import time

################################ Const ################################
def filter_value(value):
    return value.lower().replace(" ", "-")


teams = [
    'DS PENSKE', 'Jaguar TCS Racing', 'MAHINDRA RACING', 'Envision Racing',
    'Nissan Formula E Team', 'Avalanche Andretti Formula E', 'NIO 333 Racing FE Team',
    'Maserati MSG Racing', 'NEOM McLaren Formula E Team', 'ABT CUPRA FORMULA E TEAM',
    'TAG Heuer Porsche Formula E Team'
]

racers_data = [
    {
        "racer": filter_value(name),
        "team": filter_value(random.choice(teams)),
        "points": [random.randint(0, 100) for _ in range(17)]
    }
    for name in [
        "Jake Dennis", "Stoffel Vandoorne", "Sergio Camara", "Robin Frijns",
        "Jake Hughes", "Maximilian Gunther", "Sam Bird", "Mitch Evans",
        "Lucas di Grassi", "Antonio Felix da Costa", "Sébastien Buemi",
        "Norman Nato", "Jehan Daruvala", "Nyck de Vries", "Oliver Rowland",
        "Sacha Fenestraz", "Jean-Eric Vergne", "Dan Ticktum", "Nick Cassidy",
        "Edoardo Mortara", "Nico Müller", "Pascal Wehrlein"
    ]
]

app = Flask(__name__)


def run_flask():
    app.run(debug=True, use_reloader=False)


################################ Racer Functions ################################

def search_name(group_field, value):
    if not value:
        raise ValueError(f"{group_field} not informed")
    racers = []
    for racer in racers_data:
        if filter_value(value) in racer[group_field]:
            if racer["racer"] == filter_value(value):
                return racer
            racers.append(racer)

    return racers


def all_racers():
    return racers_data


def all_teams():
    return [{team: search_name("team", team)} for team in teams]


def total_points(group_type, name):
    if not name:
        raise ValueError("Name not informed")

    name = filter_value(name)
    total = 0
    for racer in racers_data:
        if racer[group_type] == name:
            total += sum(racer["points"])

    return {group_type: name, "total": total}


def top(group_type):
    if group_type == "racer":
        return top_racer()
    return top_teams()


def top_racer():
    top_racers = []
    max_points = 0
    for racer in racers_data:
        sum_points = sum(racer["points"])
        if sum_points > max_points:
            top_racers = [racer]
            max_points = sum_points
        elif sum_points == max_points:
            top_racers.append(racer)
    return {"racers": top_racers}


def top_teams():
    try:
        past_teams = []
        top_teams = []
        max_points = 0

        for racer in racers_data:
            team = racer["team"]
            if team not in past_teams:
                current = total_points("team", team)

                if current["total"] > max_points:
                    top_teams = [current]
                    max_points = current["total"]

                elif current["total"] == max_points:
                    top_teams.append(current)

                past_teams.append(team)

        return {"teams": top_teams}
    except Exception as e:
        print(e)


################################ Instagram ################################

def conn_instagram(data):
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        raise ValueError("Username and password are required")
    cl = Client()
    cl.login(username, password)
    return cl


################################ API Routes ################################

@app.route('/racer', methods=['GET'])
def get_racer():
    try:
        name = request.args.get("name")
        return jsonify(search_name("racer", name)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500


@app.route('/racers', methods=['GET'])
def get_all_racers():
    try:
        return jsonify(all_racers()), 200
    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500


@app.route('/team', methods=['GET'])
def get_team_racers():
    try:
        team = request.args.get('name')
        return jsonify(search_name("team", team)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500


@app.route('/teams', methods=['GET'])
def get_all_teams_racers():
    try:
        return jsonify(all_teams()), 200
    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500


@app.route('/top/<group_type>', methods=['GET'])
def top_info(group_type):
    try:
        if group_type not in ['team', 'racer']:
            raise ValueError("Invalid group type. Use 'team' or 'racer'.")

        return jsonify(top(group_type)), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500


@app.route('/points/<group_type>', methods=['GET'])
def get_points(group_type):
    try:
        if group_type not in ['team', 'racer']:
            raise ValueError("Invalid group type. Use 'team' or 'racer'.")

        name = request.args.get('name')

        return jsonify(total_points(group_type, name)), 200
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

################################ DearPyGui Interface ################################

def send_request(url, data=None, method='GET'):
    try:
        if method == 'GET':
            response = requests.get(url, params=data)
        else:
            response = requests.post(url, json=data)

        if response.status_code == 200:
            response_obj = json.loads(response.text)
            dpg.set_value("response_text", json.dumps(response_obj, indent=2))
        else:
            dpg.set_value("response_text", f"Failed to fetch data: {response.status_code}")
    except Exception as e:
        dpg.set_value("response_text", f"Error fetching data: {e}")


def create_input_dialog(title, label, callback, inputs):
    # Generate a unique identifier for each window based on the current time
    unique_id = str(time.time()).replace('.', '')

    # Check if the window already exists and delete it before creating a new one
    if dpg.does_item_exist(title + unique_id):
        dpg.delete_item(title + unique_id)  # Delete the window and its children

    with dpg.window(label=title, modal=True, show=True, tag=title + unique_id):  # Use title + unique_id as the unique window tag
        dpg.add_text(label)
        data = {}
        input_tags = {}

        # Create input fields with unique tags
        for input_name in inputs:
            tag = f"{input_name}_{unique_id}"  # Make the tag unique
            input_tags[input_name] = tag
            dpg.add_input_text(hint=input_name.capitalize(), tag=tag)

        def submit_callback():
            for input_name in inputs:
                tag = input_tags[input_name]
                data[input_name] = dpg.get_value(tag)  # Get value using the unique tag

            dpg.set_value("response_text", "Autenticando Usuário...")
            callback(data)

        dpg.add_button(label="Submit", callback=submit_callback)


def create_window():
    dpg.create_context()

    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_Button, [255, 20, 147])
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [255, 105, 180])
            dpg.add_theme_color(dpg.mvThemeCol_Text, [255, 255, 255])
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, [0, 0, 0])

    with dpg.window(label="Painel de Controle", width=600, height=500):
        dpg.add_text("Painel de Informações da corrida", color=[255, 20, 147], bullet=True, indent=100)
        dpg.add_separator()
        dpg.add_text("Escolha uma ação abaixo:", color=[255, 255, 255], indent=120)

        with dpg.group(horizontal=True):
            dpg.add_button(
                label="Buscar Corredor",
                callback=lambda: create_input_dialog(
                    "Buscar Corredor",
                    "Digite o nome do corredor",
                    lambda data: send_request("http://127.0.0.1:5000/racer", data),
                    ['name']),
                width=150)

            dpg.add_button(
                label="Todas os Corredores",
                callback=lambda: send_request("http://127.0.0.1:5000/racers"),
                width=150)

            dpg.add_button(
                label="Top Corredores",
                callback=lambda: send_request("http://127.0.0.1:5000/top/racer"),
                width=150)

        with dpg.group(horizontal=True):
            dpg.add_button(
                label="Buscar Equipe",
                callback=lambda: create_input_dialog(
                    "Buscar Equipe",
                    "Digite o nome da Equipe",
                    lambda data: send_request("http://127.0.0.1:5000/team", data),
                    ['name']),
                width=150)

            dpg.add_button(
                label="Todas as Equipes",
                callback=lambda: send_request("http://127.0.0.1:5000/teams"),
                width=150)

            dpg.add_button(
                label="Top Equipes",
                callback=lambda: send_request("http://127.0.0.1:5000/top/team"),
                width=150)

        with dpg.group(horizontal=True):
            dpg.add_button(
                label="Pontos de Corredor",
                callback=lambda: create_input_dialog(
                    "Pontos de Corredor",
                    "Digite o nome do corredor",
                    lambda data: send_request("http://127.0.0.1:5000/points/racer", data),
                    ['name']),
                width=150)

            dpg.add_button(
                label="Pontos de Equipe",
                callback=lambda: create_input_dialog(
                    "Pontos de Equipe",
                    "Digite o nome da equipe",
                    lambda data: send_request("http://127.0.0.1:5000/points/team", data),
                    ['name']),
                width=150)

            dpg.add_button(
                label="Conectar ao Instagram",
                callback=lambda: create_input_dialog(
                    "Conectar Instagram", "Username e Senha",
                    lambda data: send_request("http://127.0.0.1:5000/connect", data, method='POST'),
                    ['username', 'password']),
                width=150)

        dpg.add_separator()
        dpg.add_text("Response:", color=[255, 255, 255], indent=120)
        dpg.add_input_text(multiline=True, readonly=True, height=200, width=400, tag="response_text")

    dpg.bind_theme(global_theme)
    dpg.create_viewport(title='DearPyGui & Flask Communication', width=600, height=500, resizable=False)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()



################################ Main ################################

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    create_window()
