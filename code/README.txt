Multi-chromosome Genetic Algorithm

Environment:
	python 3.6
	matplotlib 2.1.1
	numpy 1.14.0
	
There are 9 files in total including 7 python files and 2 txt files.
	The 'main.py' is the main function. It initialize the population and start the iteration.
	
	In 'car_customer.py', we define the class of car and customer， and the function for loading data from two txt files('data_info.txt' and 'depot_info.txt').

	In 'cross_over.py', we define the function for cross_over.
	
	In 'function.py', there are the codes for selection, getting distance set, and showing result.
	
	In 'multichromosome.py', we define the class of Chromosome and corresponding operations.
	
	The 'mutation.py' is code for mutation. 
	
	The 'population.py' is the definition of population.
	
	In 'data_info.txt', the first line is the number of customers and vehicles. Then from line 2 to 11 is the ID of customers, his location and his need. Line 12 to 15 is the ID of vehicles and its type and which depot it belongs to.

	In 'depot_info.txt', the first line is the number of depots and the type of vehicles. Then line 2 to 4 is the ID of depots and its location. Line 5 to 7 is the ID for each type of vehicles and its capacity, its fixed cost and its variable cost.

To run the code, just run 'main.py'.