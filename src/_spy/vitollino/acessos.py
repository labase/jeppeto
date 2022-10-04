from os import walk
from os.path import join
from matplotlib import pyplot as plt
import datetime as dt
import numpy as np
# ROOT = "/home/carlo/Documentos/doc/shuttle/_access_"
ROOT = "/home/carlo/Documentos/doc/shuttle/_accessfono_"


class Access:
    def __init__(self):
        self.log = []
        self.log_count = {}
        for root, dirs, files in walk(ROOT):
            for filename in [join(root, fileid) for fileid in files]:
                log_file = open(filename)
                self.log.extend([line for line in log_file.readlines()])
            break
        print(len(self.log))
        self.pr_get = [line for line in self.log if "com/supygirls/gamer" in line]
        self.pr_get = [line.split("- [")[1].split('/2018')[0] for line in self.log if "com/supygirls/gamer" in line]
        print(len(self.pr_get))
        print(self.pr_get)
        for date in self.pr_get:
            self.log_count[date] = self.log_count[date] + 1 if date in self.log_count else 1
        self.log_pairs = [("{}{}".format(9 if "Sep" in date else 8, date.split("/")[0]), count)
                          for date, count in self.log_count.items()]
        self.log_pairs.sort()
        print(self.log_pairs)

    def splot(self):
        now = dt.date(2018, 8, 22)
        y = [b for _, b in self.log_pairs]
        days = [now + dt.timedelta(days=x) for x in np.arange(0, len(y), 1.)]
        plt.plot(days, y)
        plt.show()

    def plot(self):
        now = dt.datetime.now()
        days = [now + dt.timedelta(days=x) for x in np.arange(0, 30, 1 / 4.)]
        days_value = np.random.random(len(days))

        fig, axs = plt.subplots()
        # fig.subplots_adjust(hspace=0.75)
        axs.plot(days, days_value)

        for label in axs.get_xmajorticklabels() + axs.get_xmajorticklabels():
            label.set_rotation(30)
            label.set_horizontalalignment("right")

        fig.show()


if __name__ == '__main__':
    Access().splot()
