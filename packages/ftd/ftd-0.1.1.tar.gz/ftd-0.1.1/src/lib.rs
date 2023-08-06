use pyo3::prelude::*;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

#[pyfunction]
fn render(py: pyo3::Python, file: String, data: String) -> PyResult<&PyAny> {
    // dbg!(&data, data.get_type(), data.get_type_ptr());
    // for k in data.iter()? {
    //     let g = k?;
    //     dbg!(&g, data.get_item(g));
    // }
    pyo3_asyncio::tokio::future_into_py(py, async move {
        let config = {
            let mut config = match fpm::Config::read().await {
                Ok(c) => c,
                _ => {
                    return Ok(Python::with_gil(|py| py.None()));
                }
            };
            config.extra_data = match serde_json::from_str(data.as_str()) {
                Ok(c) => c,
                _ => {
                    return Ok(Python::with_gil(|py| py.None()));
                }
            };
            config
        };
        fpm::build(&config, Some(file.as_str()), "/", false)
            .await
            .ok();
        Ok(Python::with_gil(|py| py.None()))
    })
}

#[pyfunction]
fn fpm_build(
    py: pyo3::Python,
    file: Option<String>,
    base_url: Option<String>,
    ignore_failed: Option<bool>,
) -> PyResult<&PyAny> {
    pyo3_asyncio::tokio::future_into_py(py, async move {
        let config = match fpm::Config::read().await {
            Ok(c) => c,
            _ => {
                return Ok(Python::with_gil(|py| py.None()));
            }
        };
        fpm::build(
            &config,
            file.as_deref(),
            base_url.unwrap_or_else(|| "/".to_string()).as_str(), // unwrap okay because base is required
            ignore_failed.unwrap_or(false),
        )
        .await
        .ok();
        Ok(Python::with_gil(|py| py.None()))
    })
}

/*#[pyfunction]
fn parse(
    filename: &str,
    data: std::collections::BTreeMap<String, String>,
) -> PyResult<std::collections::BTreeMap<String, String>> {
    Ok(File {
        filename: filename.to_string(),
        data,
    })
}*/

/// A Python module implemented in Rust.
#[pymodule]
fn ftd(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_function(wrap_pyfunction!(fpm_build, m)?)?;
    // m.add_function(wrap_pyfunction!(parse, m)?)?;
    m.add_function(wrap_pyfunction!(render, m)?)?;
    Ok(())
}
