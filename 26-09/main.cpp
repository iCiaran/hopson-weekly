#include <iostream>
#include <vector>
#include <fstream>
#include <sstream>
#include <iterator>
#include <algorithm>

std::vector<int> split(const std::string& s);
int partition(std::vector<int>& list, int left, int right, int pivotIndex);
int median_five(std::vector<int>& list, int left, int right);
int pivot(std::vector<int>& list, int left, int right);
int select(std::vector<int>& list, int left, int right, int k);
int main(int argc, char **argv);

std::vector<int> split(const std::string& s) {
    std::istringstream iss{s};
    return std::vector<int>{std::istream_iterator<int>{iss}, {}};
}

int partition(std::vector<int>& list, int left, int right, int pivotIndex){
    int pivotValue = list[pivotIndex];
    std::swap(list[pivotIndex], list[right]);
    int storeIndex = left;

    for(int i = left; i < right; ++i){
        if(list[i] < pivotValue){
            std::swap(list[storeIndex], list[i]);
            ++storeIndex;
        }
    }
    std::swap(list[right], list[storeIndex]);
    return storeIndex;    
}

int median_five(std::vector<int>& list, int left, int right) {
    return 1;
}

int pivot(std::vector<int>& list, int left, int right) {
    int subRight, median;
    
    if ((right - left) < 5) return median_five(list, left, right);
    for (int i = left; i < right; i += 5) {
        subRight = i + 4;
        if (subRight > right) {
            subRight = right;
        }

        median = median_five(list, i, subRight);
        std::swap(list[subRight], list[left + (i - left) / 5]);
    }
    return select(list, left, left + (right - left)/5, (right-left)/10 + 1);
}

int select(std::vector<int>& list, int left, int right, int k){
    int pivotIndex;
    while (true) {
        if (left == right) return list[left];
        pivotIndex = partition(list, left, right, pivot(list, left, right));
        if (pivotIndex == k) {
            return list[k];
        } else if (k < pivotIndex) {
            right = pivotIndex - 1;
        } else {
            left = pivotIndex + 1;
        }
    }
    // if(left == right) {
    //     return list[left];
    // }
    // int pivotIndex = (left + right) / 2;
    // pivotIndex = partition(list, left, right, pivotIndex);
    // if(k == pivotIndex) {
    //     return list[k];
    // } else if (k < pivotIndex) {
    //     return select(list, left, pivotIndex - 1, k);
    // } else {
    //     return select(list, pivotIndex + 1, right, k);
    // }
}

int main(int argc, char **argv){
    if(argc != 3) {
        std::cout << "Usage: " << argv[0] << " filename k\n";
        return 1;
    }
    
    std::ifstream file (argv[1]);
    std::string line;
    std::getline(file, line);
    auto list = split(line);
    std::istringstream iss (argv[2]);
    int k;
    iss >> k;

    if(k > list.size()){
        std::cout << "k must be less than or equal to the number of elements in the input file\n";
        return 1;
    }

    std::cout << select(list, 0, list.size() - 1, k-1) << std::endl;
}