# Scheduling instances
# from http://mistic.heig-vd.ch/taillard/problemes.dir/ordonnancement.dir/ordonnancement
def fromTaillard(problemString):
	"""
	Convert problem instances from 
	http://mistic.heig-vd.ch/taillard/problemes.dir/ordonnancement.dir/ordonnancement

	Interleave time and machines and machine number starts at 0.
	Example input:
		Times
		 94 66 10 53 26 15 65 82 10 27 93 92 96 70 83
		 74 31 88 51 57 78  8  7 91 79 18 51 18 99 33
		  4 82 40 86 50 54 21  6 54 68 82 20 39 35 68
		 73 23 30 30 53 94 58 93 32 91 30 56 27 92  9
		 78 23 21 60 36 29 95 99 79 76 93 42 52 42 96
		 29 61 88 70 16 31 65 83 78 26 50 87 62 14 30
		 18 75 20  4 91 68 19 54 85 73 43 24 37 87 66
		 32 52  9 49 61 35 99 62  6 62  7 80  3 57  7
		 85 30 96 91 13 87 82 83 78 56 85  8 66 88 15
		  5 59 30 60 41 17 66 89 78 88 69 45 82  6 13
		 90 27  1  8 91 80 89 49 32 28 90 93  6 35 73
		 47 43 75  8 51  3 84 34 28 60 69 45 67 58 87
		 65 62 97 20 31 33 33 77 50 80 48 90 75 96 44
		 28 21 51 75 17 89 59 56 63 18 17 30 16  7 35
		 57 16 42 34 37 26 68 73  5  8 12 87 83 20 97
		Machines
		  7 13  5  8  4  3 11 12  9 15 10 14  6  1  2
		  5  6  8 15 14  9 12 10  7 11  1  4 13  2  3
		  2  9 10 13  7 12 14  6  1  3  8 11  5  4 15
		  6  3 10  7 11  1 14  5  8 15 12  9 13  2  4
		  8  9  7 11  5 10  3 15 13  6  2 14 12  1  4
		  6  4 13 14 12  5 15  8  3  2 11  1 10  7  9
		 13  4  8  9 15  7  2 12  5  6  3 11  1 14 10
		 12  6  1  8 13 14 15  2  3  9  5  4 10  7 11
		 11 12  7 15  1  2  3  6 13  5  9  8 10 14  4
		  7 12 10  3  9  1 14  4 11  8  2 13 15  5  6
		  5  8 14  1  6 13  7  9 15 11  4  2 12 10  3
		  3 15  1 13  7 11  8  6  9 10 14  2  4 12  5
		  6  9 11  3  4  7 10  1 14  5  2 12 13  8 15
		  9 15  5 14  6  7 10  2 13  8 12 11  4  3  1
		 11  9 13  7  5  2 14 15 12  1  8  4  3 10  6
	"""
	times = []
	machines = []
	appendTo = times

	for line in problemString.splitlines():
		if line.strip().lower().startswith('time'):
			pass
		elif line.strip().lower().startswith('machine'):
			appendTo = machines
		elif line.strip() == '':
			pass
		else:
			appendTo.append([int(n) for n in line.split()])

	# too much haskell omg
	# jobs = [list(zip(map(lambda x: x-1, m), t)) for m, t in zip(machines, times)]
	jobs = [[(machine-1, time) for machine, time in zip(m, t)] for m, t in zip(machines, times)]

	return '{} {}\n{}'.format(len(jobs), len(jobs[0]), 
		'\n'.join(' '.join('{} {}'.format(m, t) for m, t in job) for job in jobs))

if __name__ == '__main__':
	print(fromTaillard("""
		Times
 64 57 81 98 59 87 
 39 96 88 83 77 58
 96 66 88 60 22 92
 93 92 96 70 83 74
  4 82 40 86 50 54
 Machines
  7  2 16  3 20
  9  7 11 10 20
  2  4  5 13  1
 19 16 11  2 20
  3 11 13 16  8
 """))