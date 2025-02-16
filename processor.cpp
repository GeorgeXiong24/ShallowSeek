#include <iostream>
#include <string>
using namespace std;

bool ContainsFuck(std::string n){
    if (n.find("fuck") != std::string::npos) {
        return true;
    } else {
        return false;
    }
    //size_t length = n_str.length(); //get the length of n_str in a variable called "length"
}

int main() {
    std::string input;
    
    // Read input from stdin
    std::getline(std::cin, input);
    
    // Initialize output string
    string output;

    // Check different input conditions

    if (input == "hello" || input == "Hello" || input == "Hello!" || input == "hello!" || input == "你好" || input == "你好!") {
        output = "Hello, how can I help you?";
    } else if (input == "你是什么大模型"||input =="What large model are you" ||input =="what large model are you") {
        output = "I am ShallowSeek.";
    } else if (ContainsFuck(input)){
        output = "Please be polite motherfucker.";
    } else {
        output = "The server is busy. Please try again later.";
    }
    
    // Write output to stdout
    std::cout << output << std::endl;
    
    return 0;
}