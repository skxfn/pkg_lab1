from streamlit.web import cli as stcli
import sys
import os

if __name__ == "__main__":
	app_path = os.path.join(os.path.dirname(__file__), "app.py")
	# Launch Streamlit as if from command line; windowed app for end users
	sys.argv = [
		"streamlit",
		"run",
		app_path,
		"--server.headless=false",
	]
	sys.exit(stcli.main())

