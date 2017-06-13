import fileinput
import random

def readJobs(path=None):
    """
    Returns a problem instance specified in a textfile at path
    """
    with fileinput.input(files=path) as f:
        next(f)
        jobs = [[(int(machine), int(time)) for machine, time in zip(*[iter(line.split())]*2)]
                    for line in f if line.strip()]
    return jobs


def printJobs(jobs):
    """
    Print a problem instance.
    """
    print(len(jobs), len(jobs[0]))
    for job in jobs:
        for machine, time in job:
            print(machine, time, end=" ")
        print()


def cost(jobs, schedule):
    """
    Calculate the makespan of a schedule for a problem instance jobs.
    """
    j = len(jobs)
    m = len(jobs[0])

    tj = [0]*j   # end of previous task for each job
    tm = [0]*m   # end of previous task on each machine

    ij = [0]*j   # task to schedule next for each job

    for i in schedule:
        machine, time = jobs[i][ij[i]]
        ij[i] += 1
        start = max(tj[i], tm[machine])
        end = start + time
        tj[i] = end
        tm[machine] = end

    return max(tm)


def normalizeSchedule(jobs, partialSchedule):
    """
    Extend a partial schedule to a valid schedule.
    """

    j = len(jobs)
    m = len(jobs[0])

    occurences = [0] * j
    normalizedSchedule = []

    for t in partialSchedule:
        try:
            occurences[t]
        except IndexError:
            print('IndexError')
        if occurences[t] < m:
            normalizedSchedule.append(t)
            occurences[t] += 1
        else:
            # ignore job for now
            pass

    for t, count in enumerate(occurences):
        if count < m:
            normalizedSchedule.extend([t] * (m - count))

    return normalizedSchedule

class OutOfTime(Exception):
    pass

def randomSchedule(j, m):
    """
    Returns a random schedule for j jobs and m machines,
    """
    schedule = [i for i in list(range(j)) for _ in range(m)]
    random.shuffle(schedule)
    return schedule


def printSchedule(jobs, schedule):
    j = len(jobs)
    m = len(jobs[0])

    tj = [0]*j   # end of previous task for job
    tm = [0]*m   # end of previous task on machine

    ij = [0]*j   # task to schedule next for each job

    for i in schedule:
        try:
            jobs[i][ij[i]]
        except IndexError:
            print('A')
        machine, time = jobs[i][ij[i]]
        ij[i] += 1
        start = max(tj[i], tm[machine])
        end = start + time
        tj[i] = end
        tm[machine] = end

        print("Start job {} on machine {} at {} ending {}.".format(i, machine, start, end))

    print("Total time:", max(tm))

def prettyPrintSchedule(jobs, schedule):
    def format_job(time, jobnr):
        if time == 1:
            return '#'
        if time == 2:
            return '[]'

        js = str(jobnr)

        if 2 + len(js) <= time:
            return ('[{:^' + str(time - 2) + '}]').format(jobnr)

        return '#' * time

    j = len(jobs)
    m = len(jobs[0])

    tj = [0]*j   # end of previous task for job
    tm = [0]*m   # end of previous task on machine

    ij = [0]*j   # task to schedule next for each job

    output = [""]*m

    for i in schedule:
        machine, time = jobs[i][ij[i]]
        ij[i] += 1
        start = max(tj[i], tm[machine])
        space = start - tm[machine]
        end = start + time
        tj[i] = end
        tm[machine] = end

        output[machine] += ' ' * space + format_job(time, i)

    [print(machine_schedule) for machine_schedule in output]

    print("Total Time: ", max(tm))


def numMachines(jobs):
    return len(jobs[0])


def numJobs(jobs):
    return len(jobs)


def shuffle(x, start=0, stop=None):
    """Shuffle part of x without copy. See also random.shuffle()."""
    if stop is None or stop > len(x):
        stop = len(x)

    for i in reversed(range(start + 1, stop)):
        # pick an element in x[start: i+1] with which to exchange x[i]
        j = random.randint(start, i)
        x[i], x[j] = x[j], x[i]


def makeMask(jobs):
    mask = [0]*len(jobs)*len(jobs[0])
    ij = [0]*len(jobs)
    for i in range(len(jobs)):
        for j in range(len(jobs[0])):
            mask[i*len(jobs[0])+j]=jobs[i][j][0]
    mask.sort()
    return mask

def converterVectorToOperation(schedule,mask):
    new_schedule = list(zip(schedule,mask))
    new_schedule.sort()
    return [i[1] for i in new_schedule]


