use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use std::collections::HashMap;

#[pyfunction]
fn count(file_path: &str) -> PyResult<HashMap<String, u64>> {
    if let Ok(r) = nors::Nors::new(file_path).count() {
        let r = r.results;
        Ok(vec![
            (
                "lines".to_string(),
                *r.get(&nors::ResultType::Lines).unwrap(),
            ),
            (
                "csv_records".to_string(),
                *r.get(&nors::ResultType::CsvRecords).unwrap(),
            ),
        ]
        .into_iter()
        .collect::<HashMap<_, _>>())
    } else {
        Err(pyo3::exceptions::PyFileNotFoundError::new_err(format!(
            "File not found: {}",
            file_path
        )))
    }
}

#[pymodule]
fn nors(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(count, m)?)?;

    Ok(())
}
