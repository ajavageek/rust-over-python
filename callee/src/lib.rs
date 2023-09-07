use std::ffi::{c_char, CStr};
use std::str;

use num::Complex;

#[no_mangle]
fn compute(c_string_ptr: *const c_char, a: Complex<f64>, b: Complex<f64>) -> Complex<f64> {
    let bytes = unsafe { CStr::from_ptr(c_string_ptr).to_bytes() };
    let command = str::from_utf8(bytes).unwrap();
    match command {
        "add" => a + b,
        "sub" => a - b,
        "mul" => a * b,
        _ => panic!("Unknown command"),
    }
}
