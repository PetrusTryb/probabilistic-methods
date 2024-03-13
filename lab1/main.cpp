#include <iostream>
#include <vector>
#include <set>
using namespace std;

struct TreeNode{
	int data;
	vector<TreeNode> children;
	TreeNode(){}
	TreeNode(int data){
		this->data = data;
	}
};

void printTree(TreeNode& root, string& buffer, int &counter){
	if(root.data!=-1)
		buffer += to_string(root.data) + " ";
	if(root.children.size() == 0){
		buffer+="\n";
		counter++;
		return;
	}
	else{
		printTree(root.children[0], buffer, counter);
		if(root.children.size())
			if(root.children[0].children.size() == 0)
				root.children.erase(root.children.begin());
	}
}

void printTreeAsCombinations(TreeNode& root, int length, string& buffer, int &counter){
	set<set<int>> combinations;
	combinations.insert(set<int>());
	for(TreeNode& child:root.children){
		set<int> newSet;
		newSet.insert(child.data);
		combinations.insert(newSet);
		for(set<int> s:combinations){
			s.insert(child.data);
			combinations.insert(s);
		}
	}
	for(set<int> s:combinations){
		if(s.size() != length)
			continue;
		counter++;
		for(int i:s)
			buffer+=to_string(i)+" ";
		buffer+="\n";
	}
}

void generateTree(TreeNode& root, set<int> elements, int length, bool repetitions = false){
	if(length == 0)
		return;
	set<int> elems(elements);
	for(int i:elems){
		TreeNode newNode(i);
		if(!repetitions)
			elements.erase(i);
		generateTree(newNode, elements, length-1, repetitions);
		root.children.push_back(newNode);
		if(!repetitions)
			elements.insert(i);
	}
}

int main(){
	set<int> my_set = {1, 2, 3, 4, 5, 6};
	TreeNode root(-1);
	string output="";
	int counter = 0;

	output="Permutations of 6 elements:\n";
	counter = 0;
	generateTree(root,my_set,my_set.size());
	while(root.children.size() > 0)
		printTree(root, output, counter);
	cout<<counter<<" ";
	cout<<output<<endl;

	output="Variations of 3 elements:\n";
	counter = 0;
	generateTree(root,my_set,3);
	while(root.children.size() > 0)
		printTree(root, output, counter);
	cout<<counter<<" ";
	cout<<output<<endl;

	output="Variations of 4 elements with repetitions:\n";
	counter	= 0;
	generateTree(root,my_set,4,true);
	while(root.children.size() > 0)
		printTree(root, output, counter);
	cout<<counter<<" ";
	cout<<output<<endl;

	generateTree(root,my_set,4,true);
	output="Combinations of 4 elements:\n";
	counter = 0;
	printTreeAsCombinations(root, 4, output, counter);
	cout<<counter<<" ";
	cout<<output<<endl;
	return 0;
}