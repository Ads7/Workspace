import networkx as nx
import matplotlib.pyplot as plt
import json
import numpy as np

def union(list1,list2):
	for e in list2:
		if e not in list1:
			list1.append(e)
			

def get_page(url):
	try:
		import urllib
		return urllib.urlopen(url).read()
	except:
		return ""

def get_next_target(s):
	start_link = s.find('<a href="h')
	start_quote = s.find('"', start_link)
	end_quote = s.find('"', start_quote + 1)
	if start_quote == -1:
		return None, 0
	
	url = s[start_quote + 1:end_quote]
	s = s[end_quote:]
	return url,end_quote

def get_all_links(page):
	links_list=[]
	while True:
		url, end_pos = get_next_target(page)
		if url:
			links_list.append(url)
			page = page[end_pos:]
		else:
			break
	return links_list			

def crawl_web(seed):
	tocrawl = [seed]
	crawled = []
	index = {}
	graph={}
	while tocrawl:
		page = tocrawl.pop()		
		if page not in crawled:
			content = get_page(page)
			add_page_to_index(index, page, content)
			outlinks = get_all_links(content)
			graph[page]=outlinks
			plot_graph(graph)
			union(tocrawl, outlinks)
			crawled.append(page)
	return index, graph			

def add_to_index(index,keyword,url):
	if keyword in index:
		index[keyword].append(url)
	else:
		index[keyword]=[url]

def lookup(index,keyword):
	if keyword in index:
		return index[keyword]
	else:
		return None

def add_page_to_index(index,url,content):
	content=content.split()
	for e in content:
		add_to_index(index,e,url)	 		

def compute_ranks(graph):
	d = 0.8
	numloops = 10
	ranks={}
	npages=len(graph)
	for page in graph:
		ranks[page]=1.0/npages
	for i in range(0,numloops):
		new_ranks={}
		for page in graph:
			new_rank =(1-d)/npages
			for node in graph:
				if page in graph[node]:
					new_rank+=ranks[node]*d/len(graph[node])	
			new_ranks[page]=new_rank	
		ranks=new_ranks
	return ranks	
def plot_graph(graph):
	nodes=[]
	edges=[]
	for e in graph:
		nodes.append(e)
		for n in graph[e]:
			edges.append([e,n])
	G=nx.Graph()
	G.add_nodes_from(nodes)
	G.add_edges_from(edges)	
	node_size=1600
	node_color='blue'
	node_alpha=0.3
	node_text_size=12
	edge_color='blue'
	edge_alpha=0.3
	edge_tickness=1
	edge_text_pos=0.3
	text_font='sans-serif'
	pos = nx.spring_layout(G)
	nx.draw_networkx_nodes(G,pos,node_size=node_size,alpha=node_alpha, node_color=node_color)
	nx.draw_networkx_edges(G,pos,width=edge_tickness,alpha=edge_alpha,edge_color=edge_color)
	nx.draw_networkx_labels(G,pos,font_size=node_text_size,font_family=text_font)
	plt.show()
	nx.write_gml(G,"test.gml")
	from networkx.readwrite import json_graph
	data = json_graph.node_link_data(G)
	with open('graph.json', 'w') as f:
		json.dump(data, f, indent=4) # display	

# def make_hashtable(nbuckests):
# 	table=[]
# 	for x in xrange(0,nbuckests):
# 		table.append([])
# 	return table	
# def hash_string(keyword,nbuckests):
# 	h=0
# 	for s in keyword:
# 		h=(h+ord(s))%nbuckests
# 	return h	

# def hashtable_get_bucket(htable,keyword):
# 	return hash_string(keyword,nbuckests)

# def hashtable_add(htable,key,value):
# 	hashtable_get_bucket(htable,key).append([key,value])

# def hashtable_lookup(htable, key):
# 	bucket=hashtable_get_bucket(htable,key)
# 	for x in bucket:
# 		if x[0]==key:
# 			return 1
# 	return None	

# def hashtable_update(htable, key, value):
# 	bucket=hashtable_lookup(htable,key)
# 	for e in bucket:
# 		if e[0] == key:
# 			e[1] == value
# 			return
# 	bucket.append([key,value])		
crawl_web('https://docs.python.org')