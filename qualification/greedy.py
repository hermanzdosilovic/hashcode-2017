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

number_of_iterations = int(sys.argv[2])
best_score = 0
while number_of_iterations > 0:
    number_of_iterations -= 1
    cache_server_video_arrangement = [[False for i in range(V)] for j in range(C)]
    cache_server_availability = [X for i in range(C)]

    for endpoint_id, video_requests in enumerate(endpoint_video_request_queue):
        for number_of_requests, video_id in video_requests:
            for cache_server_id in range(C):
                if not endpoint_to_cache_server_latency[endpoint_id][cache_server_id]:
                    continue
                elif cache_server_availability[cache_server_id] - video_size[video_id] < 0:
                    continue
                cache_server_availability[cache_server_id] -= video_size[video_id]
                cache_server_video_arrangement[cache_server_id][video_id] = True
                break
        random.shuffle(endpoint_video_request_queue[endpoint_id])
    
    current_latency_save = 0
    for endpoint_id, video_requests in enumerate(endpoint_video_request_queue):
        for number_of_requests, video_id in video_requests:
            min_latency = endpoint_to_data_center_latency[endpoint_id]
            for cache_server_id in range(C):
                if not endpoint_to_cache_server_latency[endpoint_id][cache_server_id]:
                    continue
                elif not cache_server_video_arrangement[cache_server_id][video_id]:
                    continue
                min_latency = min(
                    min_latency,
                    endpoint_to_cache_server_latency[endpoint_id][cache_server_id]
                )
            current_latency_save += (endpoint_to_data_center_latency[endpoint_id] - min_latency)*number_of_requests

    current_score = round(current_latency_save/total_number_of_requests*1000) 
    if current_score > best_score:
        best_score = current_score
        print("New best score:", best_score, file=sys.stderr)
        
        f = open(sys.argv[1], "w")
        number_of_cache_servers = C - cache_server_availability.count(X)
        print(number_of_cache_servers, file=f)
        for cache_server_id in range(C):
            if cache_server_availability[cache_server_id] == X:
                continue
            print(cache_server_id, *[i for i in range(V) if cache_server_video_arrangement[cache_server_id][i]], file=f)
        f.close()
        print("Finding new best score ...")
