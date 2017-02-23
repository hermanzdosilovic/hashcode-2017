V, E, R, C, X = tuple(int(i) for i in input().split(" "))

video_size = tuple(int(i) for i in input().split(" "))

endpoint_to_data_center_latency = []
endpoint_to_cache_server_latency = [[0 for i in range(C)] for j in range(E)]
endpoint_cache_server_connection = [[] for i in range(E)]
cache_server_endpoint_connection = [[] for i in range(C)]
for e in range(E):
    Ld, K = tuple(int(i) for i in input().split(" "))
    endpoint_to_data_center_latency.append(Ld)
    for k in range(K):
        c, Lc = tuple(int(i) for i in input().split(" "))
        endpoint_to_cache_server_latency[e][c] = Lc
        endpoint_cache_server_connection[e].append(c)
        cache_server_endpoint_connection[c].append(e)

endpoint_video_request = [[] for i in range(E)]
for r in range(R):
    Rv, Re, Rn = tuple(int(i) for i in input().split(" "))
    endpoint_video_request[Re].append((Rv, Rn))

def calculate_total_latency(cache_server_videos_arrangement):
    total_latency = 0
    for endpoint_id, endpoint_requests in enumerate(endpoint_video_request):
        for video_id, number_of_requests in endpoint_requests:
            min_latency = endpoint_to_data_center_latency[endpoint_id]
            for cache_server_id in endpoint_cache_server_connection[endpoint_id]:
                if video_id in cache_server_videos_arrangement[cache_server_id]:
                    min_latency = min(min_latency, endpoint_to_cache_server_latency[endpoint_id, cache_server_id])
            total_latency += min_latency*number_of_requests
    return total_latency

def is_arrangement_valid(cache_server_videos_arrangement):
    for video_ids in cache_server_videos_arrangement:
        if sum([video_size[video_id] for video_id in video_ids]) > X:
            return False
    return True
