import math

canvas_script = """	
	<canvas id="canvas%d" width="1000" height="900" style="border:1px solid #d3d3d3;">
	Your browser does not support the HTML5 canvas tag.</canvas>

	<script>

	%s

	</script>
	<br>
	 """

categories = """	
	var c = document.getElementById("canvas%d");
	var ctx = c.getContext("2d");

	ctx.font = "14px Arial";
	ctx.fillText("Age",10,70);
	ctx.fillText("Posts Type 1 ",10,140);
	ctx.fillText("Posts Type 2 ",10,210);
	ctx.fillText("Avg Post Size",10,280);
	ctx.fillText("Avg Post Score ",10,350);
	ctx.fillText("Comment Count ",10,420);
	ctx.fillText("Comment Size ",10,490);
	ctx.fillText("Comment Score ",10,560);
	ctx.fillText("Views ",10,630);
	ctx.fillText("Upvotes",10,700);
	ctx.fillText("Downvotes ",10,770);
	ctx.fillText("Reputation",10,840);"""

category_colors = { "age" : "red",
					"post_type_1_count" : "orange",
					"post_type_2_count" : "yellow",
					"avg_post_size" : "greenyellow",
					"avg_post_score" : "green",
					"comments_count" : "seagreen",
					"avg_comment_size" : "royalblue",
					"avg_comment_score" : "blue",
					"views" : "indigo",
					"upvotes" : "purple",
					"downvotes" : "violet",
					"reputation" : "pink"
}

category_placement =  { "age" : 0,
					"post_type_1_count" : 1,
					"post_type_2_count" : 2, 
					"avg_post_size" : 3,
					"avg_post_score" : 4,
					"comments_count" : 5,
					"avg_comment_size" : 6,
					"avg_comment_score" : 7,
					"views" : 8,
					"upvotes" : 9,
					"downvotes" : 10,
					"reputation" : 11
}

circle_script = """
	ctx.beginPath();
	ctx.arc(%d, %d, %d, 0, 2 * Math.PI);
	ctx.fillStyle = '%s';
	ctx.fill();
	ctx.stroke();
"""
area_100 = 5654
spacing = 70

class CanvasGenerator(object):

	def __init__(self, attributes, centroids):
		self.attributes = attributes
		self.centroids = centroids
		self.canvas_string = ""

	def get_canvas(self):
		canvas_id = len(self.centroids)
		script_string = ""
		# ctegories
		script_string += categories % (canvas_id)
		# groups
		group_x = 120
		group_y = 30
		for i in range(0, len(self.centroids)):
			script_string += 'ctx.fillText("Group %d",%d,%d);\n' % (i, group_x + i * spacing, group_y);
			for a in range(0, len(self.attributes)):
				script_string += self.draw_circle(self.attributes[a], self.centroids[i][a], i)
		return canvas_script % (canvas_id, script_string)


	def draw_circle(self, category, radius_fraction, group):
		base_x = 150
		base_y = 70
		categore_placement = category_placement[category]
		color = category_colors[category]
		radius = (area_100 * radius_fraction / 2 / math.pi)**0.5
		return circle_script % (base_x + spacing * group, base_y + spacing * category_placement[category], radius, color )

