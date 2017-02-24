#include <cstdio>
#include <iostream>
#include <cstring>
#include <string>
#include <vector>
#include <algorithm>
#include <set>

constexpr int MAX_VIDEOS = 10000;
constexpr int MAX_ENDPOINTS = 1000;
constexpr int MAX_CACHE_SERVERS = 1000;
constexpr int MAX_REQUESTS = 1000000;

struct Request {
  int video;
  int endpoint;
  int number_of_requests;
} request;

bool cmp(const Request& r1, const Request& r2) {
  return r1.number_of_requests > r2.number_of_requests;
}

std::vector<Request> requests;
std::vector<int> cache_server_data[MAX_CACHE_SERVERS + 1]; // for each cache server contains videos
int video_size[MAX_VIDEOS + 1];
int endpoint_datacenter_latency[MAX_ENDPOINTS + 1]; // latency of endpoint to datacenter
int endpoint_cache_latency[MAX_ENDPOINTS + 1][MAX_CACHE_SERVERS + 1];
int endpoint_connected[MAX_ENDPOINTS + 1]; // endpoint(i) is connected to endpoint[i] cache servers
bool request_used[MAX_REQUESTS + 1];
bool video_used[MAX_VIDEOS + 1];

long long sum_video_size[MAX_CACHE_SERVERS + 1]; // for each cache server contains number

int V, E, R, C, X;

int main(int argc, char* argv[]) {

  memset(video_size, -1, sizeof(video_size));
  memset(endpoint_datacenter_latency, -1, sizeof(endpoint_datacenter_latency));
  memset(endpoint_cache_latency, -1, sizeof(endpoint_cache_latency));
  memset(endpoint_connected, -1, sizeof(endpoint_connected));

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
  for (int i = 0; i < R; ++i) {
    fscanf(fp_input, "%d %d %d", &request.video, &request.endpoint, &request.number_of_requests);
    requests.push_back(request);
  }
  fclose(fp_input);

  std::sort(requests.begin(), requests.end(), cmp);

  int number_of_cache_servers_used = 0;
  bool end = false;

  while (!end) {
    bool used = false;
    for (int i = 0; i < requests.size(); ++i) {
      if (!request_used[i]) {
        int video = requests[i].video;
        int endpoint = requests[i].endpoint;
        int number_of_requests = requests[i].number_of_requests;

        for (int j = 0; j < C; ++j) {
          if (~(endpoint_cache_latency[endpoint][j]) && sum_video_size[j] + video_size[video] <= X) {
            used = true;
            sum_video_size[j] += video_size[video];
            request_used[i] = true;
            cache_server_data[j].push_back(video);
          }
        }
      }
    }
    if (!used) {
      end = true;
    }
  }

  for (int i = 0; i < C; ++i) {
    if (cache_server_data[i].size()) {
      ++number_of_cache_servers_used;
    }
  }

  FILE* fp_output = fopen(argv[2], "w");
  fprintf(fp_output, "%d\n", number_of_cache_servers_used);
  for (int i = 0; i < C; ++i) {
    memset(video_used, 0x0, sizeof(video_used));
    if (cache_server_data[i].size()) {
      fprintf(fp_output, "%d", i);
      for (int j : cache_server_data[i]) {
        if(!video_used[j]) {
          fprintf(fp_output, " %d", j);
          video_used[j] = true;
        }
      }
      fprintf(fp_output, "\n");
    }
  }
  fclose(fp_output);

  return 0;
}
