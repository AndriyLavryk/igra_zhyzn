# app.py
from flask import Flask, render_template, request
from game_of_life import GameOfLife

app = Flask(__name__)
app.secret_key = 'clav'

# Instancia global (Singleton)
game = None

@app.route('/')
@app.route('/index')
def inicio():
    global game
    game = None
    return render_template('index.html')

@app.route('/live', methods=['GET', 'POST'])
def live():
    global game

    # Si viene del formulario, inicializamos o reiniciamos el juego
    if request.method == "POST":
        try:
            ancho = int(request.form.get("ancho", 15))
            altura = int(request.form.get("altura", 15))
        except (TypeError, ValueError):
            return "Error: ancho y altura deben ser números válidos", 400

        if game is None:
            game = GameOfLife(ancho, altura)


    # Cada recarga (GET) avanza una generación
    if game and game.counter:
        game.form_new_generation()
    if game:
        game.counter += 1

    return render_template(
        'live.html',
        juego=game  # pasamos el objeto completo
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
