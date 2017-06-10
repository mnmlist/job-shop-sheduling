import matplotlib.pyplot as plt
import matplotlib.patches as patches

jobs = [[(0, 4), (1, 3), (2, 5)], [(2, 4), (1, 3), (0, 4)], [(0, 6), (2, 3), (1, 3)]]
schedule = [2, 2, 0, 0, 1, 1, 0, 1, 2]
colors = ["r", "g", "b"]
patterns = ['-', '+', 'x', '\\', '*', 'o', 'O', '.']
hatchColor = [168 / 256, 175 / 256, 175 / 256]
if __name__ == '__main__':
    plt.close('all')


    def format_job(time, jobnr, ax, machine, end):
        if time == 1:
            return '#'
        if time == 2:
            return '[]'

        js = str(jobnr)
        ax.add_patch(
            patches.Rectangle(
                (end, machine),  # (x,y)
                time,  # width
                1,  # height
                hatch=patterns[jobnr],
                fill=None
            )
        )
        if 2 + len(js) <= time:
            return ('[{:^' + str(time - 2) + '}]').format(jobnr)

        return '#' * time


    j = len(jobs)
    m = len(jobs[0])

    tj = [0] * j  # end of previous task for job
    tm = [0] * m  # end of previous task on machine

    ij = [0] * j  # task to schedule next for each job

    output = [""] * m

    schedulePlot = plt.figure()

    ax1 = schedulePlot.add_subplot(111, aspect="auto")
    ax1.set_xlim(0, 25)
    ax1.set_ylim(0, 3)
    plt.legend(handles=[
        patches.Patch(facecolor=hatchColor, hatch=patterns[0], label='job 0'),
        patches.Patch(facecolor=hatchColor, hatch=patterns[1], label='job 1'),
        patches.Patch(facecolor=hatchColor, hatch=patterns[2], label='job 2')],
        handleheight=3
    )

    itt = 0

    for i in schedule:
        itt += 1
        machine, time = jobs[i][ij[i]]
        ij[i] += 1
        start = max(tj[i], tm[machine])
        space = start - tm[machine]
        end = start + time
        tj[i] = end
        tm[machine] = end

        output[machine] += ' ' * space + format_job(time, i, ax1, machine, start)
        schedulePlot.savefig('schedulePlot3*3' + str(itt) + '.png', dpi=90, bbox_inches='tight')

    [print(machine_schedule) for machine_schedule in output]

    print("Total Time: ", max(tm))
