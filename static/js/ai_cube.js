$(document).ready(function() {
	let cube = new Cube()
	renderCube(cube)

	// attach handler to all moves btns
	$('.moves_btn').click((e) => {
		var move = e.target.innerHTML;
		moveCube(cube, move)
	})

	// attach handler to init buttons
	$('#init_with_moves').click(() => {
		resetWithoutClearingInputs(cube, 'moves')
		var moves = $('#init_moves').val()
		moveCube(cube, moves)
	})
	$('#init_with_colours').click(() => {
		resetWithoutClearingInputs(cube, 'colours')
		var colours = $('#init_colours').val()
		cube = initCubeFromColours(colours)
	})

	// attach handler to solve and reset buttons
	$("#reset").click(() => {
		reset(cube)
	})

	$("#solve").click(() => {
		solve(cube)
	})
})
