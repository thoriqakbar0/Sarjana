use pyo3::prelude::*;
use std::path::Path;
use lopdf::Document;
use pdf_extract::extract_text;

#[pyclass]
struct RustPdfService {
    // No fields needed as we are not storing any state within the struct
}

#[pymethods]
impl RustPdfService {
    #[new]
    fn new() -> Self {
        RustPdfService {}
    }

    fn load_pdf(&self, path: String) -> PyResult<Vec<String>> {
        let pdf_path = Path::new(&path);
        let doc = Document::load(pdf_path).map_err(|e| PyErr::new::<pyo3::exceptions::PyIOError, _>(e.to_string()))?;
        
        let mut documents = Vec::new();
        for (page_number, _) in doc.get_pages() {
            let content = self.extract_text_from_page(&path, page_number)?;
            documents.push(content);
        }
        
        Ok(documents)
    }

    fn get_first_page_pdf_text(&self, path: String) -> PyResult<String> {
        self.extract_text_from_page(&path, 1)
    }

    fn extract_text_from_page(&self, path: &str, page_number: u32) -> PyResult<String> {
        let text = extract_text(path).map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(e.to_string()))?;
        let pages: Vec<&str> = text.split("\u{0C}").collect();
        
        if page_number == 0 || page_number > pages.len() as u32 {
            return Err(PyErr::new::<pyo3::exceptions::PyValueError, _>("Page number out of range"));
        }
        
        Ok(pages[page_number as usize - 1].to_string())
    }
}

#[pymodule]
fn rust_pdf_service(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<RustPdfService>()?;
    Ok(())
}