var viz_function = function(p) {
  p.setup = function() {
    var myCanvas = p.createCanvas(800,600)
    myCanvas.parent('viz2')
    p.noStroke()
    p.noLoop()
  }

  p.draw = function() {
    p.background(255,255,255)
    p.fill(0,255,0)
    p.ellipse(p.mouseX,p.mouseY,20,20)
  }

	p.mouseMoved = function() {
		p.redraw()
	}
}
var viz = new p5(viz_function)

