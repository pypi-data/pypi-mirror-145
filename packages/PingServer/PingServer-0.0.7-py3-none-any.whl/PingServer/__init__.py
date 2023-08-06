def start_server(**message):
  from flask import Flask
  from flask import Flask, render_template, redirect
  from threading import Thread
  if message == {}:
    message = ":)"
  app = Flask('app')
  @app.route('/')
  def Start():
    return message
  def run():
    app.run(host='0.0.0.0', port=6969)
  def webserver():
    server = Thread(target=run)
    server.start()