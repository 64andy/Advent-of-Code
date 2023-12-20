use std::collections::{HashMap, HashSet};
use std::fs::File;
use std::io::{BufRead, BufReader};

use lazy_regex::regex_captures;

/// Day 8.2 - Haunted Wasteland
///
/// Input:
///   You are given a list of Left/Right instructions (LRLRLRLRLR),
///     and a graph from parent->2-children "ABC = (DEF, GHI)".
///   Each node has 2 children, however they may be the same child "AAA = (AAA, AAA)"
///
/// Logic:
///   You start with a *list* of nodes, containing *each* node ending with "A"
///     e.g. [AAA, BCA, ...].
///   The instructions represent each move you must make (L=LeftChild, R=RightChild).
///   For each instruction, move every current node to its given child node *at the same time*.
///   If you exhaust your instructions, repeat them (e.g. "LR" means "LRLRLRLR..." forever).
///   You terminate when all your current nodes end with "Z".
///
///   Moving all of your nodes at once counts as a single step
///
/// Output:
///   Count and print how many steps it takes to reach the end

#[derive(Debug)]
struct ParsedFile {
    instructions: String,
    nodes: HashMap<u16, (u16, u16)>,
    starting_nodes: Vec<u16>,
    terminal_nodes: HashSet<u16> 
}

impl ParsedFile {
    fn parse(file: File) -> Result<ParsedFile, std::io::Error> {
        let mut file_lines = BufReader::new(file).lines();
        // First line is the instructions
        let instructions = String::from(file_lines.next().unwrap()?.trim());
        let mut nodes_str: Vec<(String, (String, String))> = vec![];
        // Then a blank line
        file_lines.next();

        for line in file_lines {
            let true_line = line?;
            let (_whole, parent, left_child, right_child) =
                regex_captures!(r"(...) = \((...), (...)\)", &*true_line).unwrap();
            nodes_str.push((parent.into(), (left_child.into(), right_child.into())));
        }

        // Map the string names to integers, for speed
        let nodes_to_num: HashMap<_, _> = nodes_str.iter()
                .map(|tuple| &tuple.0)
                .enumerate()
                .map(|pair| (pair.1, pair.0 as u16))
                .collect();

        let nodes: HashMap<_, _> = nodes_str.iter()
                .map(|tuple| {
                    (nodes_to_num[&tuple.0], (nodes_to_num[&tuple.1.0], nodes_to_num[&tuple.1.1]))
                })
                .collect();

        let starting_nodes: Vec<u16> = nodes_to_num.iter()
                .filter(|(node, _num)| node.ends_with("A"))
                .map(|(_node, num)| *num)
                .collect();
        
        let terminal_nodes: HashSet<u16> = nodes_to_num.iter()
                .filter(|(node, _num)| node.ends_with("Z"))
                .map(|(_node, num)| *num)
                .collect();
        
        Ok(ParsedFile {
            instructions,
            nodes,
            starting_nodes,
            terminal_nodes
        })
    }
}



fn main() {
    // Firstly, parse file
    let file = File::open("../input").unwrap();
    let parsed_file = ParsedFile::parse(file).unwrap();
    println!("{:?}", parsed_file);

    let mut n_steps_taken: u64 = 0;
    let graph = parsed_file.nodes;

    let mut working_nodes = parsed_file.starting_nodes;
    let terminal_nodes = parsed_file.terminal_nodes;

    for direction in parsed_file.instructions.chars().cycle() {
        if working_nodes.iter().all(|num| terminal_nodes.contains(num)) {
            break;
        }
        n_steps_taken += 1;

        if n_steps_taken % 1_000_000 == 0 {
            println!("{} million", n_steps_taken / 1_000_000);
        }
        working_nodes = working_nodes.iter()
            .map(|node|
                match direction {
                    'L' => graph[node].0,
                    'R' => graph[node].1,
                    _ => panic!("Unknown direction: {:?}", direction),
            })
            .collect();
    }
    println!("Total number of loops: {}", n_steps_taken);
}
