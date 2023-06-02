import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import csv
from Flights import Flight
import datetime
import random
from Dataframe import ExcelDataframe
import matplotlib.patches as mpatches

class Graph():
	def __init__(self) -> None:
		self.regions = {
    'Andina': ['AXM', 'BOG', 'MDE', 'PEI', 'EOH', 'UIB', 'LET', 'IBE', 'NVA', 'PPN', 'MZL', 'GYM', 'PYA', 'CRC','SJE'],
    'Caribe': ['BAQ', 'CTG', 'SMR', 'VUP', 'RCH', 'ADZ', 'CZU', 'MTR', 'LMN'],
    'Pacífico': ['BGA', 'CUC', 'BSC', 'AUC', 'LMC', 'GPI', 'TCO', 'IPI', 'CPB', 'ACD'],
    'Orinoquia': ['APO', 'VVC', 'EYP', 'MCJ', 'PVA', 'RVE', 'TME', 'PAL', 'BUN', 'PDA', 'MVP','PGT','PCR'],
    'Amazonia': ['PSO', 'LPD', 'FLA', 'LQM', 'VGZ', 'PUU'],
    'Insular': ['ADZ', 'PVA'],
    'Llanos Orientales': ['API', 'VVC', 'EYP', 'MCJ', 'PVA', 'RVE', 'TME', 'PAL', 'BUN', 'PDA', 'MVP', 'NQU', 'CAQ', 'PTX'],
    'Cafetera': ['AXM', 'MDE', 'PEI', 'UIB', 'MZL']
}



		self.colors = {
    'Andina': 'red',
    'Caribe': 'blue',
    'Pacífico': 'green',
    'Orinoquia': 'orange',
    'Amazonia': 'purple',
    'Insular': 'cyan',
    'Llanos Orientales': 'magenta',
    'Cafetera': 'brown'
}


		self.df = ExcelDataframe()

		dfc = pd.read_csv('costos.csv', sep=';',header=None,names=['origen','destino','precio'])

		self.dfc = dfc

		G = nx.DiGraph() 

		G = nx.from_pandas_edgelist(dfc,"origen","destino","precio",create_using=nx.DiGraph)

		self.Graph = G

		self.Graph.edges(data=True)
		for u, v, attrs in G.edges(data=True):
			weight_str = attrs['precio'].replace(",","")
			weight_int = int(weight_str)
			attrs['precio'] = weight_int
		self.edges= edge_labels = nx.get_edge_attributes(self.Graph, 'precio')


	def showGraph(self):
		dfc = pd.read_csv('costos.csv', sep=';', header=None, names=['origen', 'destino', 'precio'])

		G = nx.DiGraph()
		G = nx.from_pandas_edgelist(dfc, "origen", "destino", "precio", create_using=nx.DiGraph)

		self.Graph = G

		self.Graph.edges(data=True)
		for u, v, attrs in G.edges(data=True):
			weight_str = attrs['precio'].replace(",", "")
			weight_int = int(weight_str)
			attrs['precio'] = weight_int

		edge_labels = nx.get_edge_attributes(self.Graph, 'precio')
		pos = nx.spring_layout(self.Graph)
		unique_nodes = set()
		for u, v, attrs in G.edges(data=True):
			unique_nodes.add(u)
			unique_nodes.add(v)

		nx.draw_networkx_edges(self.Graph, pos)

		regions = list(self.regions.values())
		region_colors = list(self.colors.values())
		legend_patches = []
		for i, region in enumerate(regions):
			subgraph = G.subgraph(region)
			nx.draw_networkx_nodes(subgraph, pos, node_color=region_colors[i], nodelist=list(unique_nodes.intersection(subgraph.nodes)))
			legend_patch = mpatches.Patch(color=region_colors[i], label=list(self.colors.keys())[i])
			legend_patches.append(legend_patch)

		labels = nx.get_edge_attributes(G, 'precio')
		nx.draw_networkx_labels(G, pos, font_size=10)
		nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=8,rotate=False)

		plt.title('Colombian Airports by Region')
		plt.legend(handles=legend_patches)
		plt.axis('off')

		plt.show()


	def addNewRoute(self,origin,destination,price):
		line = [origin,destination,price]
		new_data_str = ';'.join(map(str, line))
		fname = 'costos.csv'
		with open(fname,mode="a",newline='') as file:
			writer = csv.writer(file)
			writer.writerow([new_data_str])
		self.__init__()

	def shortestRoute(self,origin,destination):
		try:
			G = self.Graph
			
			shortest_path = nx.shortest_path(G, source=origin, target=destination, weight='precio')

			subGraph = G.subgraph(shortest_path)

			pos = nx.spring_layout(G)

			#nx.draw(G, pos, with_labels=True, node_color='lightgreen')

			path_edges = [(shortest_path[i], shortest_path[i + 1]) for i in range(len(shortest_path) - 1)]

			#nx.draw_networkx_edge_labels(self.Graph,pos,rotate=False,edge_labels=self.edges)
			nx.draw_networkx_edges(self.Graph, pos)

			nx.draw(subGraph,pos,with_labels=False,edge_color='red',edgelist=path_edges)
			precio = 0

			for u,v,attrs in subGraph.edges(data=True):
				if (u,v) in path_edges:
					precio += attrs['precio']
			print(f'Total cost of flights is: {precio}\n')

			unique_nodes = set()
			for u, v, attrs in G.edges(data=True):
				unique_nodes.add(u)
				unique_nodes.add(v)


			regions = list(self.regions.values())
			region_colors = list(self.colors.values())
			legend_patches = []
			for i, region in enumerate(regions):
				subgraph = G.subgraph(region)
				nx.draw_networkx_nodes(subgraph, pos, node_color=region_colors[i], nodelist=list(unique_nodes.intersection(subgraph.nodes)))
				legend_patch = mpatches.Patch(color=region_colors[i], label=list(self.colors.keys())[i])
				legend_patches.append(legend_patch)

			labels = nx.get_edge_attributes(G, 'precio')
			nx.draw_networkx_labels(G, pos, font_size=10)
			nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=8,rotate=False)

			plt.title('Colombian Airports by Region')
			plt.legend(handles=legend_patches)
			plt.axis('off')

			plt.show()
			opt = int(input("Do you want to see tickets to next flight?\n1->Yes\n2->No\n"))
			if opt == 1:
				for u,v,attrs in subGraph.edges(data=True):
					if (u,v) in path_edges:
						a = self.files_generator(u,v)
						if a:
							b = a[0]
							ticketB = b.split(";")
							c = attrs['precio']
							print(f'**********************Plane Ticket**********************')
							print(f'Origin: {ticketB[0]}\nDestination: {ticketB[1]}\nAirline: {ticketB[2]}\nPlane ID: {ticketB[3]}\nTime of departure: {ticketB[4]}\nPrice: {c}\n')
						else:
							print(f'No available tickets from {u} to {v} at this time')
							break
				print()
		except nx.NetworkXNoPath:
			print(f'This is not a valid destination from the airport\n')



	def files_generator(self,ori:str,dest:str)->list:
		n = random.randint(3, 15)

		def fl_times(rute):
			times = []
			with  open(rute, mode="r") as file_csv:
				reader = csv.reader(file_csv)
				for row in reader:
					times.append(row[0].split(";")[4])
				current_hour = datetime.datetime.now().time().hour
				if times:
					nearest_flights_times = list(filter(lambda x: int(x.split(":")[0]) >= current_hour, times))
					return nearest_flights_times
				else:
					print("no flights currently available")    
				
				
		
		def list_of_nearest_fl():
			t = fl_times(rute)
			aux= []

			with  open(rute, mode="r") as file_csv:
				reader = csv.reader(file_csv)
				
				for row in reader:
					for times in t:
						if times in row[0]:
							aux.append(row[0])

				return aux

		if n > 0:
			
			rute = f'{ori}.csv'
			f_data = []
			file_data = []
			for i in range(n):
				f = Flight(ori, dest)
				each_flight = [f.airport_origin, f.airport_destiny, f.airline, f.flight_number,f.date_start]
				f_data.append(each_flight)
			for j in f_data:
				file_data.append(j)
	

			with open(rute, mode="w", newline="") as file_csv:
				writer = csv.writer(file_csv, delimiter=";")
				for row in file_data:
					writer.writerow(row)

			return list_of_nearest_fl()
		



