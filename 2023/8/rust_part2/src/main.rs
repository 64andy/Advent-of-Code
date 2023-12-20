use std::collections::HashMap;
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
    nodes: HashMap<String, (String, String)>,
}

impl ParsedFile {
    fn parse(file: File) -> Result<ParsedFile, std::io::Error> {
        let mut file_lines = BufReader::new(file).lines();
        // First line is the instructions
        let instructions = String::from(file_lines.next().unwrap()?.trim());
        let mut nodes: HashMap<String, (String, String)> = HashMap::new();
        // Then a blank line
        file_lines.next();

        for line in file_lines {
            let true_line = line?;
            let (_whole, parent, left_child, right_child) =
                regex_captures!(r"(...) = \((...), (...)\)", &*true_line).unwrap();
            nodes.insert(parent.into(), (left_child.into(), right_child.into()));
        }

        Ok(ParsedFile {
            instructions,
            nodes,
        })
    }
}

fn is_start(node: &String) -> bool {
    node.ends_with("A")
}

fn is_goal(node: &String) -> bool {
    node.ends_with("Z")
}

fn main() {
    // Firstly, parse file
    let file = File::open("../input").unwrap();
    let parsed_file = ParsedFile::parse(file).unwrap();
    println!("{:?}", parsed_file);

    let mut n_steps_taken: u64 = 0;
    let graph = parsed_file.nodes;

    let mut working_nodes = vec![];
    for node in graph.keys() {
        if is_start(&node) {
            working_nodes.push(node);
        }
    }

    for direction in parsed_file.instructions.chars().cycle() {
        if working_nodes.iter().all(|node| is_goal(*node)) {
            break;
        }
        n_steps_taken += 1;

        if n_steps_taken % 100_000 == 0 {
            println!("{}", n_steps_taken);
        }
        working_nodes = working_nodes.iter()
            .map(|node|
                match direction {
                    'L' => &graph[*node].0,
                    'R' => &graph[*node].1,
                    _ => panic!("Unknown direction: {:?}", direction),
            })
            .collect();
    }
    println!("Total number of loops: {}", n_steps_taken);
}
