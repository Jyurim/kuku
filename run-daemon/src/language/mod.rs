pub mod cpp;
pub mod java;
pub mod python;

pub use cpp::CPlusPlus;
pub use java::Java;
pub use python::Python;

#[derive(Debug)]
pub struct Submission {
    pub id: u64,
    pub language: String,
    pub input: String,
    pub code: String,
    pub status_updated: mysql_async::Value,
}
impl Submission {
    pub fn new(
        id: u64,
        language: String,
        input: String,
        code: String,
        status_updated: mysql_async::Value,
    ) -> Self {
        Self {
            id,
            language,
            input,
            code,
            status_updated,
        }
    }
}

#[derive(Debug)]
pub struct RunResult {
    pub id: u64,
    pub result: Result<String, String>,
}
impl RunResult {
    pub fn error(id: u64, error: String) -> Self {
        Self {
            id,
            result: Err(error),
        }
    }

    pub fn output(id: u64, output: String) -> Self {
        Self {
            id,
            result: Ok(output),
        }
    }
}

pub trait Language {
    fn new(submission: Submission) -> Self;

    fn run(mut self: Self) -> RunResult
    where
        Self: Sized,
    {
        unimplemented!();
    }
}
