from flask import Flask, render_template, request
import json
import subprocess
import argparse

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    try:
        with open("settings.json", "r") as f:
            settings = json.load(f)
            exec_command_template = settings.get("exec_command", "Not found")
            servers = settings.get("servers", [])
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f'Error when reading settings.json: {e}')
        exec_command_template = "Error settings"
        servers = []

    exec_result = ""
    exec_command = ""

    if request.method == "POST":
        plugin_code = request.form.get("plugin_code", "").strip()
        server_id = request.form.get("server_id", "").strip()

        if not plugin_code:
            exec_result = "Код плагина не указан"
        elif not server_id:
            exec_result = "Сервер не выбран"
        else:
            try:
                exec_command = exec_command_template.replace(
                    "PLUGIN_CODE", plugin_code).replace("SERVER_ID", server_id)

                print(f"Executing command: {exec_command}")

                completed_process = subprocess.run(
                    exec_command,
                    capture_output=True,
                    text=True,
                    check=True,
                    shell=True
                )
                exec_result = completed_process.stdout.strip()
            except subprocess.CalledProcessError as e:
                exec_result = f"Ошибка при выполнении команды:\n{e.stderr.strip() or e}"
            except Exception as e:
                exec_result = f"Непредвиденная ошибка: {e}"

    return render_template(
        "index.html",
        exec_command=exec_command or exec_command_template,
        exec_result=exec_result,
        servers=servers
    )


@app.errorhandler(Exception)
def handle_value_error(error):
    print(f"ERROR: {error}")
    try:
        with open("settings.json", "r") as f:
            settings = json.load(f)
            exec_command = settings.get("exec_command", "Not found")
            servers = settings.get("servers", [])
    except:
        exec_command = "Error"
        servers = []

    return render_template(
        "index.html",
        exec_command=exec_command,
        exec_result=str(error),
        servers=servers
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=5000)
    args = parser.parse_args()

    app.run(host='0.0.0.0', port=args.port, debug=False)
