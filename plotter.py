import matplotlib.pyplot as plt
import datetime

class Plotter:
    def __init__(self, temp_log_file, yellow_temp_edges, red_temp_edges, image_path):
        self.__temp_log = temp_log_file
        self.__yellow_edges = yellow_temp_edges
        self.__red_edges = red_temp_edges
        self.__data = []
        self.__image_path = image_path

    def _read_data(self, since, till):
        with open(self.__temp_log, 'r') as log:
            content = log.readlines()
        self.__data.clear()
        for line in content:
            date_str, time_str, temp_str, humidity_str = line.split()

            # Remove seconds and microseconds
            time_str = time_str[:-8]
            parse_date_str = date_str + " " + time_str
            try:
                date = datetime.datetime.strptime(parse_date_str, "%Y-%m-%d %H:%M:%S")
            except Exception as e:
                print("Exception " + str(e) + " while parsing <" + parse_date_str + ">")
                continue
            if since:
                if date < since:
                    continue
            if till:
                if date > till:
                    continue
            temp = float(temp_str[:-1])
            humidity = float(humidity_str[:-1])
            self.__data.append((date, temp, humidity))

    def _prepare_plot(self):
        # TODO: sort?
        start_time = self.__data[0][0]
        i = 0

        time_plot = []
        temp_plot = []
        hum_plot = []

        for time, temp, hum in self.__data:
            time_plot.append(str(time))
            temp_plot.append(temp)
            hum_plot.append(hum / 10)

        plt.plot(time_plot, temp_plot)

        # Areas
        yellow_low = self.__yellow_edges[0]
        yellow_high = self.__yellow_edges[1]
        red_low = self.__red_edges[0]
        red_high = self.__red_edges[1]
        xs = [time_plot[0], time_plot[0], time_plot[-1], time_plot[-1]]

        yellow_ys1 = [red_low, yellow_low, yellow_low, red_low]
        yellow_ys2 = [red_high, yellow_high, yellow_high, red_high]
        red_ys1 = [red_low, 0, 0, red_low]
        red_ys2 = [red_high, red_high + red_low, red_high + red_low, red_high]
        green_ys = [yellow_low, yellow_high, yellow_high, yellow_low]

        plt.fill(xs, yellow_ys1, facecolor='#FFFF0033')
        plt.fill(xs, yellow_ys2, facecolor='#FFFF0033')
        plt.fill(xs, red_ys1, facecolor='#FF000033')
        plt.fill(xs, red_ys2, facecolor='#FF000033')
        plt.fill(xs, green_ys, facecolor='#00FF0055')

        plt.plot(time_plot, hum_plot)

    def _plot(self):
        self._prepare_plot()
        plt.show()
        plt.clf()

    def _plot_to_file(self):
        self._prepare_plot()
        plt.savefig(self.__image_path, bbox_inches='tight')
        plt.clf()
        return self.__image_path


    def plot(self, since=None, till=None):
        self._read_data(since, till)
        if self.__data:
            self._plot()
        else:
            print("No data to make a plot")

    def plot_to_file(self, since=None, till=None):
        self._read_data(since, till)
        if self.__data:
            return self._plot_to_file()
        else:
            return None



#if __name__ == "__main__":
#    plotter = Plotter("temp.log", (15, 19), (12, 21), "temp.png")
#    till = datetime.datetime(2023, 10, 1, 0, 0, 0)
#    plotter.plot_to_file(till=till)
