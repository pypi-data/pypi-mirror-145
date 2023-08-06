
use pyo3::prelude::*;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

// Counts the maximum number of times ANY character in a string repeats
#[pyfunction]
fn count_max_char_repeats(val: &str) -> PyResult<(u64, char)> {
    let mut max = 0u64;
    let mut total = 0u64;
    let mut letter = ' ';

    let mut chars = val.chars();
    if let Some(mut c1) = chars.next() {
        for c2 in chars {
            if c1 == c2 {
                total += 1;
                if total > max {
                    max += 1;
                    letter = c2.clone();
                }
            } else {
                total = 0;
            }
            c1 = c2;
        }
    }

    Ok((max + 1, letter))
}

/// A Python module implemented in Rust.
#[pymodule]
fn ryayoung_util(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_function(wrap_pyfunction!(count_max_char_repeats, m)?)?;
    Ok(())
}