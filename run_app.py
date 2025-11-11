from streamlit.web import cli as stcli
import sys
import os

if __name__ == "__main__":
	app_path = os.path.join(os.path.dirname(__file__), "app.py")
	# Запуск Streamlit как из командной строки; окно браузера для пользователя
	sys.argv = [
		"streamlit",
		"run",
		app_path,
		"--server.headless=false",
	]
	sys.exit(stcli.main())

