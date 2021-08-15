const colourToFaceMap = {'y':'U', 'r':'R', 'b':'F', 'w':'D', 'o':'L', 'g':'B'} 
const faceToColourMap = {'U':'y', 'R':'r', 'F':'b', 'D':'w', 'L':'o', 'B':'g'} 

// helper functions to map from colours to face and vice versa
faceToColours = (faceString) => {
	return faceString.split('').map((char) => faceToColourMap[char]).join('')
}
coloursToFace = (colourString) => {
	return colourString.split('').map((char) => colourToFaceMap[char]).join('')
}

// renders a cube with a string of colours
initCubeFromColours = (colourString) => {
	const faceString = colourString.split('').map((char) => colourToFaceMap[char]).join('')
	const cube = Cube.fromString(faceString)
	renderCube(cube)
	return cube
}

// reset the cube
reset = (cube) => {
	cube.identity()
	renderCube(cube)
	$('#moves').html('')
	$('#init_colours').val('')
	$('#init_moves').val('')
	$('#solution').html("Solution will be displayed here")
}

// generate solution given a state
solve = (cube) => {
	const colours = faceToColours(cube.asString())
	// const url = "http://localhost:5000/solver?colours=" + colours
	const url = "/solver?colours=" + colours
	$.ajax({
		url: url,
		success: (result) => {
			if (result.success) {
				$('#solution').html("Solution found: " + result.solution)
			} else {
				$('#solution').html("No solution found ):")
			}
		}
	});
}

// move the cube
moveCube = (cube, move) => {
	cube.move(move)
	renderCube(cube)
	renderMoves(move)
}

// updates the both the front and back png of the cube, checks if its solved as well
renderCube = (cube) => {
	// get the state of the cube 
	const colors = faceToColours(cube.asString())

	// make url
	const url = "http://cube.crider.co.uk/visualcube.png?size=300&fc=" + colors

	// render cube front
	$('#cube_front').html("<img src=\"" + url + "\">")

	// render cube back
	const back_rotation = '&r=y225x34'
	$('#cube_back').html( "<img src=\"" + url + back_rotation + "\">")

	// check if the cube is solved
	checkSolved(cube)
}

// updates the move list
renderMoves = (move) => {
	const previousMoves = $('#moves').html()
	$('#moves').html(previousMoves + ' ' + move)
}

// check if the cube is solved and update the solved button (disabled lol)
checkSolved = (cube) => {
	const timems = 1500
	let cls;
	let text;
	if (cube.isSolved()) {
		cls = 'btn-success'
		text = 'SOLVED'
	} else {
		cls = 'btn-danger'
		text = 'Nope, not solved'
	}
	$('#isSolved').addClass(cls);

	setTimeout(function() {
	  $('#isSolved').removeClass(cls);
	}, timems);

	$('#isSolved').html(text)
}
