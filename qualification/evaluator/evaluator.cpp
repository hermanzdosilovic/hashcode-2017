#include <cstdio>
#include <iostream>
#include <cstring>
#include <string>
#include <vector>
#include <algorithm>

void ASSERT(bool expression, const std::string& msg, int output_line, int cache_index, int video_index) {
  if (!expression) {
    std::cout << msg << output_line << ", cache index = " << cache_index << ", video index = " << video_index << std::endl;
    exit(1);
  }
}

struct Request {
  int video;
  int endpoint;
  int number_of_requests;
} request;

constexpr int MAX_VIDEOS = 10000;
constexpr int MAX_ENDPOINTS = 1000;
constexpr int MAX_CACHE_SERVERS = 1000;
constexpr int MAX_REQUESTS = 1000000;

// used for input files
std::vector<int> cache_server_data[MAX_CACHE_SERVERS + 1]; // for each cache server contains videos
int video_size[MAX_VIDEOS + 1];
int endpoint_datacenter_latency[MAX_ENDPOINTS + 1]; // latency of endpoint to datacenter
int endpoint_cache_latency[MAX_ENDPOINTS + 1][MAX_CACHE_SERVERS + 1];
int endpoint_connected[MAX_ENDPOINTS + 1]; // endpoint(i) is connected to endpoint[i] cache servers

// used for output files
int number_of_cache_servers_used;
long long sum_video_size[MAX_CACHE_SERVERS + 1]; // for each cache server contains number

/**
● V​ (1 ≤ V ≤ 10000) - the number of videos
● E (1 ≤ E ≤ 1000) - the number of endpoints
● R (1 ≤ R ≤ 1000000) - the number of request descriptions
● C (1 ≤ C ≤ 1000) - the number of cache servers
● X (1 ≤ X ≤ 500000) - the capacity of each cache server in megabytes
*/

int V, E, R, C, X;

// cmd args = <path to input file> <path to output file>
int main(int argc, char* argv[]) {

  memset(video_size, -1, sizeof(video_size));
  memset(endpoint_datacenter_latency, -1, sizeof(endpoint_datacenter_latency));
  memset(endpoint_cache_latency, -1, sizeof(endpoint_cache_latency));
  memset(endpoint_connected, -1, sizeof(endpoint_connected));

  // handle input file
  FILE* fp_input = fopen(argv[1], "r");
  fscanf(fp_input, "%d %d %d %d %d", &V, &E, &R, &C, &X);
  for (int i = 0; i < V; ++i) {
    fscanf(fp_input, "%d", &video_size[i]);
  }
  for (int i = 0; i < E; ++i) {
    int cache_id, latency;
    fscanf(fp_input, "%d %d", &endpoint_datacenter_latency[i], &endpoint_connected[i]);
    for (int j = 0; j < endpoint_connected[i]; ++j) {
      fscanf(fp_input, "%d %d", &cache_id, &latency);
      endpoint_cache_latency[i][cache_id] = latency;
    }
  }
  //for (int i = 0; i < R; ++i) {
  //  fscanf(fp_input, "%d %d %d", &requests[i].video, &requests[i].endpoint, &requests[i].number_of_requests);
  //}
  //fclose(fp_input);

  int current_cache = -1;
  int output_line = 0;
  int first;
  char second;

  FILE* fp_output = fopen(argv[2], "r");
  fscanf(fp_output, "%d", &number_of_cache_servers_used);
  //printf("number_of_cache_servers_used = %d\n", number_of_cache_servers_used);
  while (output_line <= number_of_cache_servers_used) {
    fscanf(fp_output, "%d%c", &first, &second);

    if (~current_cache) {
      sum_video_size[current_cache] += video_size[first];
      //printf("cache id = %d, cache size = %d\n", current_cache, sum_video_size[current_cache]);
      ASSERT(sum_video_size[current_cache] <= X, "Maximum cache size excceded! Line = ", output_line, current_cache, first);
      cache_server_data[current_cache].push_back(first);
    }

    if (current_cache == -1) {
      current_cache = first;
    }

    if (second == '\n') {
      current_cache = -1;
      ++output_line;
    }
  }
  fclose(fp_output);

  printf("\nOutput is correct!\n");

  for (int i = 0; i < C; ++i) {
    std::sort(cache_server_data[i].begin(), cache_server_data[i].end());
  }

  long long total_time_in_miliseconds{0ULL};
  long long total_time_saved{0ULL};
  long long total_number_of_requests{0ULL};

  while (fscanf(fp_input, "%d %d %d", &request.video, &request.endpoint, &request.number_of_requests) == 3) {
    int min_time = endpoint_datacenter_latency[request.endpoint];
    for (int i = 0; i < C; ++i) {
      if (~endpoint_cache_latency[request.endpoint][i]) {
        if (std::binary_search(cache_server_data[i].begin(), cache_server_data[i].end(), request.video)) {
          min_time = std::min(min_time, endpoint_cache_latency[request.endpoint][i]);
        }
      }
    }
    total_time_saved += (endpoint_datacenter_latency[request.endpoint] - min_time) * request.number_of_requests;
    total_number_of_requests += request.number_of_requests;
  }

  printf("Total time saved: %lld microseconds!\n\n", static_cast<long long>((total_time_saved * 1000.0) / total_number_of_requests));
  return 0;
}
