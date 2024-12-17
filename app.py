from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Algoritmul FCFS
def fcfs(processes):
    n = len(processes)
    completion_time = []    
    waiting_time = []        
    execution_order = []     
    step_durations = []     
    
    named_processes = [(f"P{i+1}", burst_time) for i, burst_time in enumerate(processes)]

    current_time = 0
    
    for process in named_processes:
        execution_order.append(process[0])  
        current_time += process[1]         
        completion_time.append(current_time)
        step_durations.append(process[1])   

    for i in range(n):
        waiting_time.append(completion_time[i] - named_processes[i][1])

    avg_waiting_time = sum(waiting_time) / n
    avg_completion_time = sum(completion_time) / n

    return {
        "execution_order": execution_order,
        "step_durations": step_durations,
        "completion_time": completion_time,
        "waiting_time": waiting_time,
        "avg_waiting_time": avg_waiting_time,
        "avg_completion_time": avg_completion_time
    }

def sjf(burst_times):
    n = len(burst_times)
    process_names = [f"P{i+1}" for i in range(n)] 
    processes = list(zip(process_names, burst_times)) 

    processes.sort(key=lambda x: x[1])

    completion_time = []  
    waiting_time = []    
    execution_order = []  
    step_durations = []   

    current_time = 0  
    for process in processes:
        process_name, burst_time = process
        execution_order.append(process_name)
        step_durations.append(burst_time)  
        current_time += burst_time
        completion_time.append(current_time)

    for i, (_, burst_time) in enumerate(processes):
        waiting_time.append(completion_time[i] - burst_time)

    avg_completion_time = sum(completion_time) / n
    avg_waiting_time = sum(waiting_time) / n

    return {
        "execution_order": execution_order,
        "step_durations": step_durations,
        "completion_time": completion_time,
        "waiting_time": waiting_time,
        "avg_completion_time": avg_completion_time,
        "avg_waiting_time": avg_waiting_time
    }

# Algoritmul Cel mai scurt timp ramas (SRTF)
def srtf(burst_times, quantum):
    n = len(burst_times)  
    process_names = [f"P{i+1}" for i in range(n)] 
    processes = list(zip(process_names, burst_times)) 
    
    remaining_time = [process[1] for process in processes] 
    process_queue = [(i, processes[i][1]) for i in range(n)]  
    order_of_execution = []  
    step_durations = [] 
    time = 0 

    while process_queue:
        process_queue.sort(key=lambda x: (x[1], x[0]))
        current_process_idx, current_burst_time = process_queue.pop(0)

        executed_time = min(current_burst_time, quantum)
        remaining_time[current_process_idx] -= executed_time
        time += executed_time

        order_of_execution.append(processes[current_process_idx][0]) 
        step_durations.append(executed_time)

        if remaining_time[current_process_idx] > 0:
            process_queue.append((current_process_idx, remaining_time[current_process_idx]))

    weighted_sum = 0
    num_steps = len(step_durations)
    
    for i in range(num_steps):
        weighted_sum += (num_steps - i) * step_durations[i]

    avg_completion_time = weighted_sum / num_steps

    cumulative_waiting_times = [0]
    for i in range(1, num_steps):
        cumulative_waiting_times.append(cumulative_waiting_times[-1] + step_durations[i - 1])

    sum_cumulative_waiting_times = sum(cumulative_waiting_times)
    
    avg_waiting_time = sum_cumulative_waiting_times / n

    completion_times = []
    current_time = 0
    for duration in step_durations:
        current_time += duration
        completion_times.append(current_time)

    # Return the results
    return {
        "execution_order": order_of_execution,
        "step_durations": step_durations,
        "completion_time": completion_times, 
        "waiting_time": cumulative_waiting_times,
        "avg_completion_time": avg_completion_time,
        "avg_waiting_time": avg_waiting_time
    }

# Algoritmul Round Robin - RR
def round_robin(burst_times, quantum):
    n = len(burst_times)
    process_names = [f"P{i+1}" for i in range(n)] 
    processes = list(zip(process_names, burst_times))  

    remaining_burst_times = burst_times.copy() 
    execution_order = []  
    step_durations = []  
    time = 0  

    while any(remaining_burst_times):  
        for i in range(n):
            if remaining_burst_times[i] > 0:
                execution_order.append(processes[i][0]) 
                time_slice = min(remaining_burst_times[i], quantum) 
                step_durations.append(time_slice)
                remaining_burst_times[i] -= time_slice
                time += time_slice

    waiting_time = [0]  
    for i in range(1, len(step_durations)):
        waiting_time.append(waiting_time[-1] + step_durations[i - 1])

    completion_time = []
    current_time = 0
    for duration in step_durations:
        current_time += duration
        completion_time.append(current_time)

    # Calculate averages
    avg_completion_time = sum(completion_time) / len(completion_time)
    avg_waiting_time = sum(waiting_time) / n

    return {
        "execution_order": execution_order,
        "step_durations": step_durations,
        "completion_time": completion_time,
        "waiting_time": waiting_time,
        "avg_completion_time": avg_completion_time,
        "avg_waiting_time": avg_waiting_time
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        process_times_str = request.form['process_time']
        quantum = int(request.form.get('quantum', 0))  
        
        processes = [int(x.strip()) for x in process_times_str.split(',')]
        
        selected_algorithm = request.form.get('algorithm', 'fcfs') 

        if selected_algorithm == 'fcfs':
            results = fcfs(processes)
        elif selected_algorithm == 'sjf':
            results = sjf(processes)
        elif selected_algorithm == 'srtf':
            results = srtf(processes, quantum)
        elif selected_algorithm == 'rr':
            results = round_robin(processes, quantum)

        return jsonify(results) 

    return render_template('index.html', processes=[], selected_algorithm='fcfs')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8000)