use std::ffi::{c_char, c_double, CStr};
use std::str;

use num::Complex;

#[no_mangle]
fn compute(
    c_string_ptr: *const c_char,
    c_a_real: c_double,
    c_a_imag: c_double,
    c_b_real: c_double,
    c_b_imag: c_double,
) -> Complex<f64> {
    let bytes = unsafe { CStr::from_ptr(c_string_ptr).to_bytes() };
    let command = str::from_utf8(bytes).unwrap();
    let a: Complex<f64> = Complex {
        re: c_a_real,
        im: c_a_imag,
    };
    let b: Complex<f64> = Complex {
        re: c_b_real,
        im: c_b_imag,
    };
    match command {
        "add" => a + b,
        "sub" => a - b,
        "mul" => a * b,
        _ => panic!("Unknown command"),
    }
}
