import random
import sys

V, E, R, C, X = tuple(int(i) for i in input().split(" "))

video_size = tuple(int(i) for i in input().split(" "))

endpoint_to_data_center_latency = []
endpoint_to_cache_server_latency = [[0 for i in range(C)] for j in range(E)]
for e in range(E):
    Ld, K = tuple(int(i) for i in input().split(" "))
    endpoint_to_data_center_latency.append(Ld)
    for k in range(K):
        c, Lc = tuple(int(i) for i in input().split(" "))
        endpoint_to_cache_server_latency[e][c] = Lc

endpoint_video_request = [[0 for i in range(V)] for j in range(E)]
total_number_of_requests = 0
for r in range(R):
    Rv, Re, Rn = tuple(int(i) for i in input().split(" "))
    endpoint_video_request[Re][Rv] = Rn
    total_number_of_requests += Rn

endpoint_video_request_queue = [[] for i in range(E)]
for endpoint_id in range(E):
    endpoint_video_request_queue[endpoint_id] = [(x, i) for i, x in enumerate(endpoint_video_request[endpoint_id]) if x]
    endpoint_video_request_queue[endpoint_id].sort(reverse=True)

best_latency = max(endpoint_to_data_center_latency)*total_number_of_requests
number_of_iterations = int(sys.argv[2])
while number_of_iterations > 0:
    number_of_iterations -= 1
    cache_server_video_arrangement = [[False for i in range(V)] for j in range(C)]
    cache_server_availability = [X for i in range(C)]
    endpoint_video_latency = [[0 for i in range(V)] for j in range(E)]
    current_latency = 0
    for i in range(E):
        for j in range(V):
            endpoint_video_latency[i][j] = endpoint_to_data_center_latency[i]*endpoint_video_request[i][j]
            current_latency += endpoint_video_latency[i][j]

    for endpoint_id, video_requests in enumerate(endpoint_video_request_queue):
        for number_of_requests, video_id in video_requests:
            for cache_server_id in range(C):
                if not endpoint_to_cache_server_latency[endpoint_id][cache_server_id]:
                    continue
                elif cache_server_availability[cache_server_id] - video_size[video_id] < 0:
                    continue
                cache_server_availability[cache_server_id] -= video_size[video_id]
                cache_server_video_arrangement[cache_server_id][video_id] = True
                
                for dependent_endpoint_id in range(E):
                    latency = endpoint_to_cache_server_latency[dependent_endpoint_id][cache_server_id]
                    if not latency:
                        continue
                    if not endpoint_video_request[dependent_endpoint_id][video_id]:
                        continue
                    current_latency -= endpoint_video_latency[dependent_endpoint_id][video_id]
                    endpoint_video_latency[dependent_endpoint_id][video_id] = min(
                        endpoint_video_latency[dependent_endpoint_id][video_id],
                        latency*endpoint_video_request[dependent_endpoint_id][video_id]
                    )
                    current_latency += endpoint_video_latency[dependent_endpoint_id][video_id]
                break
        random.shuffle(endpoint_video_request_queue[endpoint_id])
                
    if current_latency < best_latency:
        best_latency = current_latency
        print("New best latency:", best_latency, file=sys.stderr)
        
        f = open(sys.argv[1], "w")
        number_of_cache_servers = C - cache_server_availability.count(X)
        print(number_of_cache_servers, file=f)
        for cache_server_id in range(C):
            print(cache_server_id, end=" ", file=f)
            for video_id in range(V):
                if cache_server_video_arrangement[cache_server_id][video_id]:
                    print(video_id, end=" ", file=f)
            print(file=f)
        f.close()
        print("Finding new best latency ...")
