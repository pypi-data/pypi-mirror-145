import os

import numpy as np
from numpy import inf
from numpy import nan

import pandas as pd

from . import Plotting

class EvalTool(object):

    def __init__(self, experiment_name):

        self.experiment_name = experiment_name

        # Plot params configurable by user

        # Plot N Results
        self.plot_n_res_scale  = "both"
        self.plot_n_res_ylabel = "Number of Results"
        self.plot_n_res_xticks = True

        # Plot Query times
        self.plot_query_time_scale  = "both"
        self.plot_query_time_ylabel = "Average Query Time(s)"
        self.plot_query_time_xticks = True

        # Plot Query Throughput
        self.plot_query_throughput_scale  = "both"
        self.plot_query_throughput_ylabel = "Queries per second"
        self.plot_query_throughput_xticks = True

        # Plot Results Throughput
        self.plot_n_res_throughput_scale  = "both"
        self.plot_n_res_throughput_xticks = True

        # Plot Speedup
        self.plot_speedup_scale  = "none"
        self.plot_speedup_xticks = True

        try:
            self.data = pd.read_csv(experiment_name + ".csv")
        except:
            print("File not found, creating a new onself...")
            self.data = pd.DataFrame(columns=[
                    "query", "engine", "db_size",
                    "n_threads",
                    "n_samples",
                    "query_time_avg", "query_time_std",
                    "n_results", "n_results_std",
                    ])

            self.export_to_csv()

    def remove_n_threads(self, th_arr=[]):

        for th in th_arr:
            self.data = self.data[self.data.n_threads != th]

    def subsample_db_sizes(self, decimation=10):

        self.new_ev = EvalTool(self.experiment_name + "_subsampled")
        self.new_ev.clear()

        threads  = self.get_unique("n_threads")
        queries  = self.get_unique("query")
        engines  = self.get_unique("engine")

        new_max = None
        new_min = None
        for eng in engines:
            for th in threads:
                for q in queries:

                    db_sizes  = self.get_arr_for_eng_q_threads(eng, q, th,
                                                                "db_size")
                    samples   = self.get_arr_for_eng_q_threads(eng, q, th,
                                                                "n_samples")
                    times     = self.get_arr_for_eng_q_threads(eng, q, th,
                                                                "query_time_avg")
                    times_std = self.get_arr_for_eng_q_threads(eng, q, th,
                                                                "query_time_std")
                    n_results = self.get_arr_for_eng_q_threads(eng, q, th,
                                                                "n_results")
                    n_results_std = self.get_arr_for_eng_q_threads(eng, q, th,
                                                                "n_results_std")

                    for i in range(0,len(db_sizes),decimation):

                        self.new_ev.add_row(q, eng, db_sizes[i], th, samples[0],
                                     times[i], times_std[i],
                                     n_results[i], n_results_std[i])

        self.new_ev.export_to_csv()
        self.data = pd.read_csv(self.experiment_name + "_subsampled.csv")

    # This method will make sure only the common set of db_sizes are present.
    def cleanup_db_sizes(self):

        threads  = self.get_unique("n_threads")
        queries  = self.get_unique("query")
        engines  = self.get_unique("engine")

        new_max = None
        new_min = None
        for eng in engines:
            for th in threads:
                for q in queries:
                    db_sizes  = self.get_arr_for_eng_q_threads(eng, q, th,
                                                                "db_size")
                    largest  = db_sizes[-1]
                    if new_max is None:
                        new_max = largest
                    else:
                        if largest < new_max:
                            new_max = largest

                    smallest = db_sizes[0]
                    if new_min is None:
                        new_min = smallest
                    else:
                        if smallest > new_min:
                            new_min = smallest

        self.data = self.data[self.data.db_size <= new_max]
        self.data = self.data[self.data.db_size >= new_min]

    # This method will subsumple db_sizes, using the specified range_size
    def pre_process_db_sizes(self, range_size=0):

        self.new_ev = EvalTool(self.experiment_name + "_processed")
        self.new_ev.clear()

        threads  = self.get_unique("n_threads")
        queries  = self.get_unique("query")
        engines  = self.get_unique("engine")

        for eng in engines:
            for th in threads:
                for q in queries:

                    db_sizes  = self.get_arr_for_eng_q_threads(eng, q, th,
                                                                "db_size")
                    samples   = self.get_arr_for_eng_q_threads(eng, q, th,
                                                                "n_samples")
                    times     = self.get_arr_for_eng_q_threads(eng, q, th,
                                                                "query_time_avg")
                    n_results = self.get_arr_for_eng_q_threads(eng, q, th,
                                                                "n_results")

                    times_arr = []
                    n_results_arr = []
                    range_end  = range_size

                    for (size,i) in zip(db_sizes, range(len(db_sizes))):

                        if size < range_end:
                            times_arr.append(times[i])
                            n_results_arr.append(n_results[i])

                        else:
                            new_time     = np.mean(times_arr)
                            new_time_std = np.std(times_arr)

                            new_n_results     = np.mean(n_results_arr)
                            new_n_results_std = np.std(n_results_arr)

                            self.new_ev.add_row(q, eng, range_end, th, samples[0],
                                         new_time, new_time_std,
                                         new_n_results, new_n_results_std)

                            times_arr = []
                            n_results_arr = []

                            times_arr.append(times[i])
                            n_results_arr.append(n_results[i])

                            range_end += range_size

                    if len(times_arr) > 0:

                        new_time     = np.mean(times_arr)
                        new_time_std = np.std(times_arr)

                        new_n_results     = np.mean(n_results_arr)
                        new_n_results_std = np.std(n_results_arr)

                        self.new_ev.add_row(q, eng, range_end, th, samples[0],
                                     new_time, new_time_std,
                                     new_n_results, new_n_results_std)

                        times_arr = []
                        n_results_arr = []

                        times_arr.append(times[i])
                        n_results_arr.append(n_results[i])

                        range_end += range_size

        self.new_ev.cleanup_db_sizes()
        self.new_ev.export_to_csv()
        self.data = pd.read_csv(self.experiment_name + "_processed.csv", index_col=0)

    def set_log_scale(self, val):

        self.plot_n_res_scale             = val
        self.plot_query_time_scale        = val
        self.plot_query_throughput_scale  = val
        self.plot_n_res_throughput_scale  = val

    def set_log_scale_for_x_only(self):

        self.plot_n_res_scale             = "x"
        self.plot_query_time_scale        = "x"
        self.plot_query_throughput_scale  = "x"
        self.plot_n_res_throughput_scale  = "x"

    def set_log_scale_for_y_only(self):

        self.plot_n_res_scale             = "y"
        self.plot_query_time_scale        = "y"
        self.plot_query_throughput_scale  = "y"
        self.plot_n_res_throughput_scale  = "y"

    def set_xticks(self, val=True):
        self.plot_n_res_xticks            = val
        self.plot_query_time_xticks       = val
        self.plot_query_throughput_xticks = val
        self.plot_n_res_throughput_xticks = val

    def add_row(self, query, engine, db_size,
            n_threads,
            n_samples,
            query_time_avg, query_time_std,
            n_results, n_results_std):

        self.data.loc[len(self.data)] = [
                query,
                engine,
                db_size,
                n_threads,
                n_samples,
                query_time_avg,
                query_time_std,
                n_results,
                n_results_std,
            ]

    def clear(self):

        self.data = pd.DataFrame(columns=[
                    "query", "engine", "db_size",
                    "n_threads",
                    "n_samples",
                    "query_time_avg", "query_time_std",
                    "n_results", "n_results_std",
                    ])

        self.export_to_csv()

    def export_to_csv(self):

        self.data.to_csv(self.experiment_name + ".csv", index=False)

    def get_unique(self, column):

        arr = []
        vals = self.data.loc[:,column]

        # arr = [v for v in vals if v not in arr]
        for val in vals:
            if val not in arr:
                arr.append(val)

        return arr

    def get_arr_for_eng_q_dbsize(self, engine, query, db_size, key):

        arr = self.data[self.data["query"] == query]
        arr = arr[self.data["engine"]      == engine]
        arr = arr[self.data["db_size"]     == db_size]
        arr = arr[key].to_numpy()

        return arr

    def get_arr_for_eng_q_threads(self, engine, query, threads, key):

        arr = self.data[self.data["query"] == query]
        arr = arr[self.data["engine"]      == engine]
        arr = arr[self.data["n_threads"]   == threads]
        arr = arr[key].to_numpy()

        return arr

    def get_arr_for_eng_q_threads(self, engine, query, threads, key):

        arr = self.data[self.data["query"] == query]
        arr = arr[self.data["engine"]      == engine]
        arr = arr[self.data["n_threads"]   == threads]
        arr = arr[key].to_numpy()

        return arr

    def plot_all(self, folder="plots"):
        self.plot_folder=folder
        self.plot_folder += "/"

        if not os.path.exists(self.plot_folder):
            os.makedirs(self.plot_folder)

        self.plot_all_for_db_size()
        self.plot_all_for_n_clients()
        self.plot_all_for_all_queries()

    def plot_all_for_all_queries(self):

        threads  = self.get_unique("n_threads")
        queries  = self.get_unique("query")

        if len(queries) == 1:
            return

        print("Plotting plot_all_for_all_queries...")

        for q in queries:
            self.plot_results_throughput_parallelism_threads(q, result_type="Images")


    def plot_all_for_n_clients(self):

        threads  = self.get_unique("n_threads")
        queries  = self.get_unique("query")

        if len(threads) == 1:
            return

        db_sizes = self.get_unique("db_size")

        print("Plotting plot_all_for_n_clients...")

        for i in db_sizes:

            self.plot_results_throughput_parallelism_queries(i, result_type="Images")

        for i in queries:
            self.plot_results_throughput_parallelism_dbsizes(i, result_type="Images")
            self.plot_results_n_results_parallelism_dbsizes(i)

    def plot_all_for_db_size(self):

        db_sizes = self.get_unique("db_size")

        if len(db_sizes) == 1:
            return

        threads = self.get_unique("n_threads")

        print("Plotting plot_all_for_db_size...")

        for i in threads:

            try:
                self.plot_query_time(i)
            except:
                print("Error plotting:", "plot_query_time")
            try:
                self.plot_query_throughput(i)
            except:
                print("Error plotting:", "plot_query_throughput")
            try:
                self.plot_results_throughput(i, result_type="Images")
            except:
                print("Error plotting:", "plot_results_throughput")
            try:
                self.plot_query_time_speedup(i)
            except:
                print("Error plotting:", "plot_query_time_speedup")
            try:
                self.plot_n_results(i)
            except:
                print("Error plotting:", "plot_n_results")

    def plot_results_throughput_parallelism_threads(self, q,
                                            result_type="results"):

        # Plot query times:
        threads  = self.get_unique("n_threads")
        queries  = self.get_unique("query")
        engines  = self.get_unique("engine")
        db_sizes = self.get_unique("db_size")

        # Todo make general for more db_sizes
        values = np.zeros(len(db_sizes) * 2)

        for eng in engines:
            for th in threads:

                times     = self.get_arr_for_eng_q_threads(eng, q, th,
                                                            "query_time_avg")
                times_std = self.get_arr_for_eng_q_threads(eng, q, th,
                                                            "query_time_std")
                n_results = self.get_arr_for_eng_q_threads(eng, q, th,
                                                            "n_results")

                # Compute Results per second
                rps   = 1/times * th * n_results
                rps[rps == inf] = 0

                stds  = rps * (times_std / times)

                # print("values:",len(values, len(values[0])))
                # print("rps:",len(rps))

                values = np.vstack((values, np.append(rps, stds)))

        values = values[1:,:] # remove initial row of zeros

        p = Plotting.Plotting()

        # filename  = self.plot_folder + "plot_conc_q_"
        # filename += str(q) + "_results_throughput_threads.pdf"

        # title = "Throughput as " + result_type + " per second Summary"
        # p.plot_lines_all(str(threads), db_sizes, engines, values,
        #                   title=title,
        #                   filename=filename,
        #                   log="both",
        #                   xlabel="Database Size",
        #                   ylabel=result_type + "/s")

        filename  = self.plot_folder + "plot_q_"
        filename += str(q) + "_mosaic_results_throughput_threads.pdf"

        threads = ["clients: " + str(a) for a in threads]
        # title = "Throughput for " + q
        # title += " as Database Size increases"
        p.plot_lines_all_mosaic(threads, db_sizes, engines, values,
                          filename=filename,
                          # title=title,
                          log="both",
                          xlabel="Database Size",
                          ylabel=result_type + "/s")



    def plot_results_throughput_parallelism_dbsizes(self, q,
                                            result_type="results"):

        # Plot query times:
        threads  = self.get_unique("n_threads")
        queries  = self.get_unique("query")
        engines  = self.get_unique("engine")
        db_sizes = self.get_unique("db_size")

        # Todo make general for more db_sizes
        values = np.zeros(len(threads) * 2)

        for eng in engines:
            for db_size in db_sizes:

                times     = self.get_arr_for_eng_q_dbsize(eng, q, db_size,
                                                            "query_time_avg")
                times_std = self.get_arr_for_eng_q_dbsize(eng, q, db_size,
                                                            "query_time_std")
                threads   = self.get_arr_for_eng_q_dbsize(eng, q, db_size,
                                                            "n_threads")
                n_results = self.get_arr_for_eng_q_dbsize(eng, q, db_size,
                                                            "n_results")

                # Compute Results per second
                rps   = 1/times * threads * n_results
                rps[rps == inf] = 0

                stds  = rps * (times_std / times)

                values = np.vstack((values, np.append(rps, stds)))

        values = values[1:,:] # remove initial row of zeros

        p = Plotting.Plotting()

        filename  = self.plot_folder + "plot_conc_q_"
        filename += str(q) + "_results_throughput_db_size.pdf"

        title = "Throughput as " + result_type + " per second - Summary"
        p.plot_lines_all(db_sizes, threads, engines, values,
                          title=title,
                          filename=filename,
                          xlabel="# of concurrent clients",
                          ylabel=result_type + "/s")

        filename  = self.plot_folder + "plot_conc_q_"
        filename += str(q) + "_mosaic_results_throughput_db_size.pdf"

        # title = "Throughput for " + q
        # title += " as number of concurrent clients increases"
        p.plot_lines_all_mosaic(db_sizes, threads, engines, values,
                          filename=filename,
                          # title=title,
                          xlabel="# of concurrent clients",
                          ylabel=result_type + "/s")

    def plot_results_n_results_parallelism_dbsizes(self, q):

        # Plot query times:
        threads  = self.get_unique("n_threads")
        queries  = self.get_unique("query")
        engines  = self.get_unique("engine")
        db_sizes = self.get_unique("db_size")

        # Todo make general for more db_sizes
        values = np.zeros(len(threads) * 2)

        for eng in engines:
            for db_size in db_sizes:

                n_results = self.get_arr_for_eng_q_dbsize(eng, q, db_size,
                                                            "n_results")
                n_results_std = self.get_arr_for_eng_q_dbsize(eng, q, db_size,
                                                            "n_results_std")

                values = np.vstack((values, np.append(n_results, n_results_std)))

        values = values[1:,:] # remove initial row of zeros

        p = Plotting.Plotting()

        filename  = self.plot_folder + "plot_conc_q_"
        filename += str(q) + "_n_results_db_size.pdf"

        title = "Number of results - Summary"
        p.plot_lines_all(db_sizes, threads, engines, values,
                          log="none",
                          title=title,
                          filename=filename,
                          ylabel=self.plot_n_res_ylabel,
                          xlabel="# of concurrent clients",
                          )

        filename  = self.plot_folder + "plot_conc_q_"
        filename += str(q) + "_mosaic_n_results_db_size.pdf"

        # title = "Throughput for " + q
        # title += " as number of concurrent clients increases"
        p.plot_lines_all_mosaic(db_sizes, threads, engines, values,
                          log="none",
                          filename=filename,
                          # title=title,
                          ylabel=self.plot_n_res_ylabel,
                          xlabel="# of concurrent clients")

    def plot_results_throughput_parallelism_queries(self, db_size,
                                            result_type="results"):

        # Plot query times:
        threads  = self.get_unique("n_threads")
        queries  = self.get_unique("query")
        engines  = self.get_unique("engine")

        # Todo make general for more db_sizes
        values = np.zeros(len(threads) * 2)

        for eng in engines:
            for q in queries:

                times     = self.get_arr_for_eng_q_dbsize(eng, q, db_size,
                                                            "query_time_avg")
                times_std = self.get_arr_for_eng_q_dbsize(eng, q, db_size,
                                                            "query_time_std")
                threads   = self.get_arr_for_eng_q_dbsize(eng, q, db_size,
                                                            "n_threads")
                n_results = self.get_arr_for_eng_q_dbsize(eng, q, db_size,
                                                            "n_results")
                stds      = self.get_arr_for_eng_q_dbsize(eng, q, db_size,
                                                            "n_results_std")

                # Compute Results per second
                rps   = 1/times * threads * n_results
                rps[rps == inf] = 0

                stds  = rps * (times_std / times)

                values = np.vstack((values, np.append(rps, stds)))

        values = values[1:,:] # remove initial row of zeros

        p = Plotting.Plotting()

        filename  = self.plot_folder + "plot_conc_dbsize_"
        filename += str(db_size) + "_results_throughput.pdf"

        title = "Throughput as " + result_type + " per second - Summary"
        p.plot_lines_all(queries, threads, engines, values,
                          title=title,
                          filename=filename,
                          xlabel="# of concurrent clients",
                          ylabel=result_type + "/s")

        filename  = self.plot_folder + "plot_conc_dbsize_"
        filename += str(db_size) + "_mosaic_results_throughput.pdf"

        # title = "Throughput for " + db_size
        # title += " as number of concurrent clients increases"
        p.plot_lines_all_mosaic(queries, threads, engines, values,
                          filename=filename,
                          # title=title,
                          xlabel="# of concurrent clients",
                          ylabel=result_type + "/s")


    def plot_results_throughput(self, n_threads, result_type="results"):

        # Plot query times:
        db_sizes = self.get_unique("db_size")
        queries  = self.get_unique("query")
        engines  = self.get_unique("engine")

        # Todo make general for more db_sizes
        values = np.zeros(len(db_sizes) * 2)

        for eng in engines:
            for q in queries:

                times     = self.get_arr_for_eng_q_threads(eng, q, n_threads,
                                                            "query_time_avg")
                times_std = self.get_arr_for_eng_q_threads(eng, q, n_threads,
                                                            "query_time_std")
                n_results = self.get_arr_for_eng_q_threads(eng, q, n_threads,
                                                            "n_results")

                # Compute Results per second
                rps   = 1/times * n_threads * n_results
                rps[rps == inf] = 0

                stds  = rps * (times_std / times)

                values = np.vstack((values, np.append(rps, stds)))

        values = values[1:,:] # remove initial row of zeros

        p = Plotting.Plotting()

        filename  = self.plot_folder
        filename += "plot_th_" + str(n_threads) + "_results_throughput.pdf"

        title = "Throughput as " + result_type + " per second - Summary"
        p.plot_lines_all(queries, db_sizes, engines, values,
                          log=self.plot_n_res_throughput_scale,
                          title=title,
                          filename=filename,
                          ylabel=result_type + "/s",
                          xticks=self.plot_n_res_throughput_xticks)

        filename  = self.plot_folder
        filename += "plot_th_" + str(n_threads) + "_mosaic_results_throughput.pdf"

        # title = "Throughput for different queries"
        p.plot_lines_all_mosaic(queries, db_sizes, engines, values,
                          log=self.plot_n_res_throughput_scale,
                          # title=title,
                          filename=filename,
                          xlabel="Database Size",
                          ylabel=result_type + "/s",
                          xticks=self.plot_n_res_throughput_xticks)


    def plot_query_throughput(self, n_threads):

        # Plot query times:
        db_sizes = self.get_unique("db_size")
        queries  = self.get_unique("query")
        engines  = self.get_unique("engine")

        values = np.zeros(len(db_sizes) * 2)

        for eng in engines:
            for q in queries:

                times   = self.get_arr_for_eng_q_threads(eng, q, n_threads,
                                                            "query_time_avg")
                stds    = self.get_arr_for_eng_q_threads(eng, q, n_threads,
                                                            "query_time_std")

                qps = 1/times * n_threads
                qps[qps == inf] = 0

                stds  = qps * (stds / times)

                values = np.vstack((values, np.append(qps, stds)))

        values = values[1:,:] # remove initial row of zeros

        p = Plotting.Plotting()

        filename  = self.plot_folder
        filename += "plot_th_" + str(n_threads) + "_queries_throughput.pdf"

        title = "Query Throughput (q/s) Summary"
        p.plot_lines_all(queries, db_sizes, engines, values,
                          log=self.plot_query_throughput_scale,
                          title=title,
                          filename=filename,
                          ylabel=self.plot_query_throughput_ylabel,
                          xticks=self.plot_query_throughput_xticks)

        filename  = self.plot_folder
        filename += "plot_th_" + str(n_threads) + "_mosaic_query_throughput.pdf"

        # title = "Query Throughput (q/s) for different queries"
        p.plot_lines_all_mosaic(queries, db_sizes, engines, values,
                          log=self.plot_query_throughput_scale,
                          # title=title,
                          filename=filename,
                          xlabel="Database Size",
                          ylabel=self.plot_query_throughput_ylabel,
                          xticks=self.plot_query_throughput_xticks
                          )


    def plot_query_time(self, n_threads):

        # Plot query times:
        db_sizes = self.get_unique("db_size")
        queries  = self.get_unique("query")
        engines  = self.get_unique("engine")

        values = np.zeros(len(db_sizes) * 2)

        for eng in engines:
            for q in queries:

                times = self.get_arr_for_eng_q_threads(eng,q, n_threads,
                                                            "query_time_avg")
                stds  = self.get_arr_for_eng_q_threads(eng, q, n_threads,
                                                            "query_time_std")

                values = np.vstack((values, np.append(times, stds)))

        values = values[1:,:] # remove initial row of zeros

        p = Plotting.Plotting()

        filename  = self.plot_folder
        filename += "plot_th_" + str(n_threads) + "_query_times.pdf"

        title = "Query Execution Time(s) Summary"
        p.plot_lines_all(queries, db_sizes, engines, values,
                          log=self.plot_query_time_scale,
                          title=title,
                          filename=filename,
                          ylabel=self.plot_query_time_ylabel,
                          xticks=self.plot_query_time_xticks)

        filename  = self.plot_folder
        filename += "plot_th_" + str(n_threads) + "_mosaic_query_times.pdf"

        # title = "Query Execution Time(s) for different queries"
        p.plot_lines_all_mosaic(queries, db_sizes, engines, values,
                          log=self.plot_query_time_scale,
                          # title=title,
                          filename=filename,
                          xlabel="Database Size",
                          ylabel=self.plot_query_time_ylabel,
                          xticks=self.plot_query_time_xticks)

        return


    def plot_n_results(self, n_threads):

        # Plot query times:
        db_sizes = self.get_unique("db_size")
        queries  = self.get_unique("query")
        engines  = self.get_unique("engine")

        values = np.zeros(len(db_sizes) * 2)

        for eng in engines:
            for q in queries:

                n_res = self.get_arr_for_eng_q_threads(eng, q, n_threads,
                                                            "n_results")
                stds  = self.get_arr_for_eng_q_threads(eng, q, n_threads,
                                                            "n_results_std")

                values = np.vstack((values, np.append(n_res, stds)))

        values = values[1:,:] # remove initial row of zeros

        p = Plotting.Plotting()

        filename  = self.plot_folder
        filename += "plot_th_" + str(n_threads) + "_n_results.pdf"

        title = "Returned Results Summary"
        p.plot_lines_all(queries, db_sizes, engines, values,
                          log=self.plot_n_res_scale,
                          title=title,
                          filename=filename,
                          ylabel=self.plot_n_res_ylabel,
                          xticks=self.plot_n_res_xticks)

        filename  = self.plot_folder
        filename += "plot_th_" + str(n_threads) + "_mosaic_n_results.pdf"

        title = "Returned Results for different queries"
        p.plot_lines_all_mosaic(queries, db_sizes, engines, values,
                          log=self.plot_n_res_scale,
                          title=title,
                          filename=filename,
                          xlabel="Database Size",
                          ylabel=self.plot_n_res_ylabel,
                          xticks=self.plot_n_res_xticks)

        return

    # Bar plot
    def plot_query_time_speedup(self, n_threads):

        # Plot query times:
        db_sizes = self.get_unique("db_size")
        engines  = self.get_unique("engine")

        if len(engines) < 2:
            print("Single engine, no speedup plot generated")
            return

        # This will only compute speedup of eng[0] vs eng[i > 0].

        for sub_eng in range(1,len(engines)):

            # We need to get queries every times because we append "avg"
            queries  = self.get_unique("query")

            s_engines = [engines[0], engines[sub_eng]]
            values = np.zeros(len(db_sizes) * 2)

            for eng in s_engines:
                for q in queries:

                    times = self.get_arr_for_eng_q_threads(eng, q, n_threads,
                                                            "query_time_avg")
                    stds  = self.get_arr_for_eng_q_threads(eng, q, n_threads,
                                                            "query_time_std")

                    values = np.vstack((values, np.append(times, stds)))

            values = values[1:,:] # remove initial row of zeros

            # Compute speedup
            for i in range(len(queries)):
                values[i,:] = values[len(queries)+i, :] / values[i, :]

            values = values[0:len(queries),:]

            # compute average and add "avg" row to queries
            avgs = np.mean(values, axis=0)
            values = np.vstack((values, avgs))
            queries.append("avg")

            p = Plotting.Plotting()

            filename  = self.plot_folder
            filename += "plot_th_" + str(n_threads) + "_query_times_speedup_"
            filename += s_engines[1] + ".pdf"

            title  = "Speedup of " + s_engines[0] + " over " + s_engines[1]
            title += " for all queries"
            p.plot_bars(queries, db_sizes, values,
                        filename=filename,
                        title=title,
                        log=self.plot_speedup_scale)

        return
