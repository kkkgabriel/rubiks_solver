from flask import Flask, render_template, url_for, jsonify, request
import rubiks_solver
app = Flask(__name__)

# path to render the cube ui
@app.route('/')
def index():
    return render_template('cube.html')

# api to generate solution
@app.route('/solver')
def solver():
	if 'colours' in request.args:
		state = request.args['colours']
		solution = rubiks_solver.solve(state)
		success = False
		if solution:
			success = True
		return jsonify({"succcess": True, "initial state": state, "Solution": solution})


if __name__ == '__main__':
	app.run(debug=True)