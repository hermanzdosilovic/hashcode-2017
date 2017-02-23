V, E, R, C, X = tuple(int(i) for i in input().split(" "))

video_size = tuple(int(i) for i in input().split(" ")) # 1 x V

endpoint_to_data_center_latency = [] # 1 x E
endpoint_to_cache_server_latency = [[0 for i in range(C)] for j in range(E)] # E x C
endpoint_cache_server_connection = [[] for i in range(E)] # 1 x E
cache_server_endpoint_connection = [[] for i in range(C)] # 1 x C
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

