import sys
import os
from monitor import Monitor
import time
import pandas as pd
import plotly.express as px
import plotly
import plotly.graph_objects as go
from plot import *

def main():
    min_num_states = int(sys.argv[1])
    max_num_states = int(sys.argv[2])
    step_num_states = int(sys.argv[3])
    # min_num_trans = int(sys.argv[4])
    # max_num_trans = int(sys.argv[5])
    # step_num_trans = int(sys.argv[6])
    # min_num_labels = int(sys.argv[7])
    # max_num_labels = int(sys.argv[8])
    # step_num_labels = int(sys.argv[9])
    min_trace_length = int(sys.argv[4])
    max_trace_length = int(sys.argv[5])
    step_trace_length = int(sys.argv[6])
    repetitions = int(sys.argv[7])
    # storm = True if sys.argv[8] == 'storm' else False
    with open('results.csv', 'w') as results:
        results.write('model_size,trace_length,monitor_synthesis_time [sec],monitor_time_prism [sec],monitor_time_per_event_prism [sec],monitor_time_storm [sec],monitor_time_per_event_storm [sec]\n')
    for states in range(min_num_states, max_num_states, step_num_states):
        # for transitions in range(max(states, min_num_trans), max_num_trans, step_num_trans):
            # for labels in range(min_num_labels, min(states, max_num_labels), step_num_labels):
        os.system(f'python3 my_genprism.py {states}')
        for trace in range(min_trace_length, max_trace_length, step_trace_length):
            synthesis_time = 0.0
            execution_time_prism = 0.0
            execution_time_storm = 0.0
            for _repetition in range(0, repetitions):
                start = time.time()
                os.system('prism ' + './meta_model.prism' + ' -exportstates ' + './meta_model.sta' + ' -exporttrans ' + './meta_model.tra' + ' -exportlabels ' + './meta_model.lab')
                monitor = Monitor('./meta_model.sta', './meta_model.tra', './meta_model.lab', './meta_model.csl', False)
                end = time.time()
                synthesis_time += end-start
                start = time.time()
                monitor.simulated_next(trace)
                end = time.time()
                execution_time_prism += end-start
                monitor = Monitor('./meta_model.sta', './meta_model.tra', './meta_model.lab', './meta_model.csl', True)
                start = time.time()
                monitor.simulated_next(trace)
                end = time.time()
                execution_time_storm += end-start
            with open('results.csv', 'a') as results:
                results.write(f'{states},{trace},')
                results.write(str(synthesis_time/repetitions) + ',')
                results.write(str(execution_time_prism/repetitions) + ',')
                results.write(str((execution_time_prism/repetitions)/trace) + ',')
                results.write(str(execution_time_storm/repetitions) + ',')
                results.write(str((execution_time_storm/repetitions)/trace) + '\n')

def generate_plots():
    df = pd.read_csv('./results.csv')

    plot_monitor_synthesis_time(df)    
    plot_monitor_execution_time(df)
    plot_monitor_execution_time_per_event(df)
    plot_monitor_time_per_trace(df)
    plot_monitor_time_per_event_per_trace(df)
    
if __name__ == "__main__":
    main()
    generate_plots()