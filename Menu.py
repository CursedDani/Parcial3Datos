from AeropuertosBack import Graph
from time import sleep
from Dataframe import ExcelDataframe
import textwrap

class Menu():
    def __init__(self) -> None:
        self.df = ExcelDataframe()
        self.database = Graph()

    def mainMenu(self):
        def showMenu():
            uopt = input(f'Please, select an option!\n1)Show all airports\n2)Show most economic route between airports\n3)Add new route\n0)Exit\n')
            return int(uopt)

        print("********Welcome to AirportDB!********")
        while True:
            sleep(1)
            opt = showMenu()
            if opt == 1:
                self.database.showGraph()
            elif opt == 2:
                self.mostEconomic()
            elif opt == 3:
                self.addNewRoute()
            elif opt == 0:
                print("Exiting...\n")
                break
            else:
                print("Invalid option, please try again\n")

    def addNewRoute(self):
        print(f'All airports: : \n')
              
        airports = self.df.getAirports()
        num_columns = 5
        excelIATA = self.df.getIATA()
        for i, airport in enumerate(airports):
            wrapped_airport = textwrap.fill(airport, width=50)
            print(f"{excelIATA[i]} | {wrapped_airport:<30}", end="" if (i + 1) % num_columns != 0 else "\n")
        print("\n")


        origin = input("Enter origin airport city:\n")

        oriIata= self.df.searchCity(origin)
        if oriIata == False:
            return
        dest = input("Enter destination airpot city:\n")
        destIata = self.df.searchCity(dest)
        price = int(input("Enter price of new route:\n"))
        self.database.addNewRoute(oriIata,destIata,price)

    def mostEconomic(self):

        dests = []
        def findNeighbors(ori):
            l = list(self.database.Graph.neighbors(ori))
            for i in l:
                if self.df.searchAirportName(i) not in dests:
                    dests.append(f'{i} | {self.df.searchAirportName(i)}')
                    findNeighbors(i)
                
        print(f'Available airports are: \n')
              
        airports = self.df.getAirports()
        num_columns = 5
        excelIATA = self.df.getIATA()
     
        graphIATA = list(self.database.dfc["origen"])

        for i, airport in enumerate(airports):
            if excelIATA[i] in graphIATA:
                wrapped_airport = textwrap.fill(airport, width=50)
                print(f"{wrapped_airport:<30}", end="" if (i + 1) % num_columns != 0 else "\n")
        print("\n")      

        origin = input("Enter origin airport city:\n")
        oriIata= self.df.searchCity(origin)
        if oriIata == False:
            return
        findNeighbors(oriIata)
        print(f'The available destinations from this airport are: \n')
        if dests:
            for i in dests:
                print(i, end=", ")
        dest = input("\nEnter destination airpot city:\n")
        destIata = self.df.iatawithname(dest)

        self.database.shortestRoute(oriIata,destIata)


                