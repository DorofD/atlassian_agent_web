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
            exec_command = settings.get("exec_command", "Not found")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f'Error when reading settings.json: {e}')
        exec_command = "Error settings"

    exec_result = ""
    if request.method == "POST":
        plugin_code = request.form.get("plugin_code")
        if plugin_code:
            try:
                exec_command_with_plugin = exec_command.replace(
                    "PLUGIN_CODE", plugin_code)
                exec_command_list = exec_command_with_plugin.split(' ')
                print(exec_command_with_plugin)
                completed_process = subprocess.run(
                    exec_command_list,
                    capture_output=True,
                    text=True,
                    check=True
                )
                exec_result = completed_process.stdout.strip()
            except subprocess.CalledProcessError as e:
                exec_result = f"Error when execution command: {e}"
        else:
            exec_result = "Код плагина не указан"

    return render_template("index.html", exec_command=exec_command, exec_result=exec_result)


@app.errorhandler(Exception)
def handle_value_error(error):
    print(f"ERROR: {error}")
    return render_template("index.html", exec_command="Error", exec_result=error)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=5000)
    args = parser.parse_args()

    app.run(host='0.0.0.0', port=args.port, debug=False)
