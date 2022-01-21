import heapq

#defining the function to read from the input file
def readFromFile(filename):

	#Maintain a list of each file line
	lines = []
	with open(f'{filename}.txt') as f:
		for line in f:
			#allocating the lines in the list
			lines.append(line.strip().split())

	#storing number of machines and list of jobs in list
	intervals = []
	for x in range(0, len(lines)):
		if x == 0:
			#first line holds machine number, so we address to it with index 0
			intervals.append(int(lines[x][0]))
		else:
			#other remaining lines have job intervals, starting from 1 to end
			intervals.append([int(lines[x][0]),int(lines[x][1])])

	return intervals

def mergeSort(jobs):

	#check if there is more that 1 job
	if len(jobs) > 1:

		# Finding the mid of the jobs
		mid = len(jobs)//2

		# Assing left half to the list L
		L = jobs[:mid]

		# Assing right half to the list R
		R = jobs[mid:]

		# Sorting the first half
		mergeSort(L)

		# Sorting the second half
		mergeSort(R)

		i = j = k = 0

		# Iterating throught the both half arrays and compare their elements base of finish time
		while i < len(L) and j < len(R):
			#if finish time of left job is less than right job
			if L[i][1] < R[j][1]:
				jobs[k] = L[i]
				i += 1

			#if finishing times are equal, then check their start time
			elif L[i][1] == R[j][1]:
				if L[i][0] < R[j][0]:
					jobs[k] = L[i]
					i += 1
				else:
					jobs[k] = R[j]
					j += 1
			# if finish time of left job is greater than right job
			else:
				jobs[k] = R[j]
				j += 1
			k += 1

		# Checking if any element left in L sub array
		while i < len(L):
			jobs[k] = L[i]
			i += 1
			k += 1

		# Checking if any element left in R sub array
		while j < len(R):
			jobs[k] = R[j]
			j += 1
			k += 1

#Declaring the main scheduling function
def Schedule(filename):

	#reading data from input file and storing it in jobs list
	jobs = readFromFile(filename)[1:]

	#keeping track of non completed jobs
	no_complete_jobs = []

	#reading input from input file and store it in this variable
	num_of_machines = readFromFile(filename)[0]

	print("Jobs before the sort")
	print(jobs,"\n")

	#sorting array
	mergeSort(jobs)
	print("Jobs after the sort")
	print(jobs,"\n")

	#declaring a heap data structure
	my_heap =[]

	#Keeping track of the jobs assigned to the machines with dictionary
	dict = {}

	#initializing the finish time of all machines, by default all have finish time 0
	for i in range(1, num_of_machines+1):
		my_heap.append([0,i])

	#Assinging empty list of jobs to each machines
	for x in range(1, num_of_machines+1):
		dict[x] = []

	#Iterating throught the jobs
	for job in jobs:

		#we pop the min finishing machine (the machine that finishes the allotted job earliest)
		value = heapq.heappop(my_heap)

		#if we can assign the job(i) to that machine, we update its finish time and push it back to the heap
		if value[0]<=job[0]:
			heapq.heappush(my_heap,[job[1],value[1]])
			#we also append that job to the list of completed jobs of that machine in dictionary
			dict[value[1]].append(job)
		else:
			#if we cannot assing the job(i) to earliest finishing machine, then we cannot assign it any machine as jobs are sorted by earliest finishing times.
			heapq.heappush(my_heap,[value[0],value[1]])

			#As result we add that job to the list of jobs NON COMPLETE
			no_complete_jobs.append(job)


	# printing dictionary of which machine performed which job and a log of the jobs that could not be performed and their numbers.
	with open("output.txt", "w") as external_file:
		for x in dict:
			assigning =f"Machine {x} did jobs: {dict[x]}"
			print(assigning,"\n")
			add_text1 = assigning
			print(add_text1, "\n", file=external_file)

	# return full list of non complete jobs
	ncompl_jobs=f"Number of non complete jobs{no_complete_jobs}"
	print(ncompl_jobs,"\n")

	#calculates and return the number of completed jobs
	compl_jobs= f"{len(jobs)-len(no_complete_jobs)} number of jobs out of {len(jobs)} total jobs \n"
	print(compl_jobs)

	#storing the output in an output file
	with open("output.txt", "a") as external_file:
		add_text2 = ncompl_jobs
		add_text3 = compl_jobs
		print(add_text2, "\n", add_text3, file= external_file)
		external_file.close()

Schedule("input4")
