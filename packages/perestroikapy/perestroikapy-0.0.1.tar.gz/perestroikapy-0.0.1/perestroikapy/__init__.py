from PIL import Image as img

def test():
	print('test')

def read_img(target):
	image = img.open(target)
	graph = image.load()
	image.close()
	return graph

def draw_line(graph, a, b, color):
	slope = (b[0]-a[0])/(b[1]-a[1])
	yi = (a[0]*slope)-a[1]
	for i in range(a[0], b[0]):
		graph[i, (i*slope)+yi] = color

	return graph

def write_img(target, graph):
	image = img.open(target)
	image.save(graph)
	image.close()