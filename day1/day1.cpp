#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <algorithm>
#include <vector>
#include <map>
#include <queue>

int main() {

    // everything used is from standard library, so save the time
    using namespace std;
    // load file
    ifstream file;
    vector<string> lines;
    string line;

    // error handling
    file.exceptions(ifstream::badbit | ifstream::failbit);

    try {
        file.open("day1_input.txt");
        while (getline(file, line)) {
            lines.push_back(line);
        }
    } catch (ifstream::failure e) {
        runtime_error("Failed to open file!");
    }

    vector<int> l1(lines.size());
    vector<int> l2(lines.size());

    string d1_s, d2_s;

    for (const auto& line: lines) {
        istringstream iss(line);
        getline(iss, d1_s, ' ');
        getline(iss, d2_s);

        l1.push_back(stoi(d1_s));
        l2.push_back(stoi(d2_s));
    }

    // first we'll get the result of part 2 since we need to convert
    // them into heaps in part 1

    map<int, int> cnt;
    for (const auto& d2: l2) {
        cnt[d2]++;
    }

    long long int similarity_score {}; 
    for (const auto& d1: l1) {
        similarity_score += d1 * cnt[d1];
    }

    priority_queue<int, vector<int>, greater<int>> min_heap1;
    priority_queue<int, vector<int>, greater<int>> min_heap2;

    // push our vectors into the heaps
    for (const auto& n: l1) {
        min_heap1.push(n);
    }

    for (const auto& n: l2) {
        min_heap2.push(n);
    }

    long long int distance {};
    while (!min_heap1.empty()) {
        distance += abs(min_heap1.top() - min_heap2.top());
        min_heap1.pop();
        min_heap2.pop();
    }

    cout << "Distance: " << distance << endl;
    cout << "Similarity Score: " << similarity_score << endl;
    
    return 0;
}
