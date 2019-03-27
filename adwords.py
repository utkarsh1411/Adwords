import csv
import sys
import random
import math
from copy import deepcopy

random.seed(0)

if len(sys.argv) < 2:
    print("Usage: python adwords.py method_name")
    print("method_name can be either 'greedy', 'msvv' or 'balance'")
    exit()

def main():
	
	queriesList = []
	totRevenue = 0
	
	with open('queries.txt') as queries:
		for q in queries:
			queriesList.append(q.strip())
	

	
	highestBids, highestAdvertiserBudgets, query = readDataset()
	
	if sys.argv[1] == 'greedy':
		totRevenue = greedy(queriesList, query, highestAdvertiserBudgets)		
		revenues = []
		for i in range(100):
			random.shuffle(queriesList)
			revenues.append(greedy(queriesList, query, highestAdvertiserBudgets))
		averageRevenue = sum(revenues)/100


	elif sys.argv[1] == 'msvv':
		
		totRevenue = msvv(queriesList, query, highestAdvertiserBudgets, highestBids)
		revenues = []
		for i in range(100):
			random.shuffle(queriesList)
			revenues.append(msvv(queriesList, query, highestAdvertiserBudgets, highestBids))
		averageRevenue = sum(revenues)/100
    
	elif sys.argv[1] == 'balance':
		totRevenue = balance(queriesList, query, highestAdvertiserBudgets)
		
		revenues = []
		for i in range(100):
			random.shuffle(queriesList)
			revenues.append(balance(queriesList, query, highestAdvertiserBudgets))
		averageRevenue = sum(revenues)/100
		
		
	else:
		print('Invalid method. Please try again.')
		exit()

	opt = sum(highestAdvertiserBudgets.values())

	print('Revenue:', round(totRevenue, 2))

	competitve_ratio = averageRevenue/opt
	print('Comp Ratio:', round(competitve_ratio, 2))
	
		

def readDataset():
	highestBids = {}
	highestAdvertiserBudgets = {}
	query = {}
	with open('bidder_dataset.csv') as highestBidding:
		reader = csv.reader(highestBidding)
	
		next(reader) 
		for row in reader:

			if row[1] not in query:
				query[row[1]] = [(int(row[0]), float(row[2]))]
			else:
				query[row[1]].append(((int(row[0]),float(row[2]))))

			if (int(row[0])) not in highestAdvertiserBudgets:
				budget = float(row[3])
				highestAdvertiserBudgets[(int(row[0]))] = budget
				highestBids[(int(row[0]))] = 0.0
	return (highestBids, highestAdvertiserBudgets, query)


def greedy(queriesList, query, highestAdvertiserBudgets):
	revenue = 0
	query = deepcopy(query)
	highestAdvertiserBudgets = deepcopy(highestAdvertiserBudgets)
	for key in query:
		query[key] = sorted(query[key], key = lambda x:x[1], reverse = True)
		queryCopy = deepcopy(query)
		highestAdvertiserBudgetsCopy = deepcopy(highestAdvertiserBudgets)
	for q in queriesList:
		queryNeighbors = query[q]
		for neighbors in queryNeighbors:
			initial = highestAdvertiserBudgets[neighbors[0]]
			if initial - neighbors[1] >= 0:
				highestAdvertiserBudgets[neighbors[0]] = initial - neighbors[1]
				revenue = revenue + neighbors[1]
				break
	
	return revenue 


def msvv(queriesList, query, highestAdvertiserBudgets, highestBids):
	revenue = 0
	query = deepcopy(query)
	highestAdvertiserBudgets = deepcopy(highestAdvertiserBudgets)
	highestBids = deepcopy(highestBids)
	for q in queriesList:
		queryNeighbors = query[q]
		highestValue = -sys.maxsize
		highestAdvertiser = 0
		highestBid = 0
		for neighbors in queryNeighbors:
			Xu = 1 - math.exp(highestBids[neighbors[0]] / highestAdvertiserBudgets[neighbors[0]] - 1)
			
			if Xu * neighbors[1] > highestValue :
				highestValue = Xu * neighbors[1]
				highestAdvertiser = neighbors[0]
				highestBid = neighbors[1]
		
		highestBids[highestAdvertiser] = highestBids[highestAdvertiser] + highestBid
		revenue = revenue + highestBid
	return revenue


def balance(queriesList, query, highestAdvertiserBudgets):
	query = deepcopy(query)
	highestAdvertiserBudgets = deepcopy(highestAdvertiserBudgets)
	revenue = 0
	for q in queriesList:
		queryNeighbors = query[q]
		Highestunspent = -sys.maxsize
		highestBid = -sys.maxsize
		highestAdvertiser = -sys.maxsize
		
		for neighbors in queryNeighbors:
			
			if highestAdvertiserBudgets[neighbors[0]] > Highestunspent :
				Highestunspent = highestAdvertiserBudgets[neighbors[0]]
				highestAdvertiser = neighbors[0]
				highestBid = neighbors[1]
		
		if Highestunspent - highestBid >= 0:
			highestAdvertiserBudgets[highestAdvertiser] = Highestunspent - highestBid
			revenue = revenue + highestBid
	return revenue


if __name__ == "__main__":
	main()