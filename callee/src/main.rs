use num::Complex;
use serde::{Deserialize, Serialize};
use std::fs::{metadata, remove_file};
use std::io::{Read, Write};
use std::os::unix::net::UnixListener;

#[tokio::main]
async fn main() {
    let srv_path = "/tmp/socket";
    if metadata(srv_path).is_ok() {
        remove_file(srv_path).unwrap();
    }
    let listener = UnixListener::bind(srv_path).unwrap();
    loop {
        let (mut stream, _) = listener.accept().unwrap();
        let mut payload = String::new();
        let _ = stream.read_to_string(&mut payload);
        println! {"Received {}", payload};
        let input = serde_json::from_str::<Input>(&payload).unwrap();
        let output = &command(input);
        let result = serde_json::to_string(output).unwrap();
        stream.write(result.as_bytes()).unwrap_or_default();
        println! {"Sent {}", result};
    }
}

fn command(json: Input) -> Output {
    let command = json.command;
    let result = match command {
        "add" => json.a + json.b,
        "sub" => json.a - json.b,
        "mul" => json.a * json.b,
        _ => panic!("Unknown command"),
    };
    Output { result }
}

#[derive(Deserialize)]
struct Input<'a> {
    command: &'a str,
    a: Complex<f64>,
    b: Complex<f64>,
}

#[derive(Serialize)]
struct Output {
    result: Complex<f64>,
}
