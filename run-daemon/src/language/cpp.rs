use super::{Language, RunResult, Submission};
use std::{io::Write, process};

#[derive(Debug)]
pub struct CPlusPlus {
    submission: Submission,
}

impl Language for CPlusPlus {
    fn new(submission: Submission) -> Self {
        Self { submission }
    }

    fn run(mut self: Self) -> RunResult
    where
        Self: Sized,
    {
        let filename = format!("kuku-{}.cpp", self.submission.id);
        let file = std::fs::File::create(format!("/tmp/{}", filename));
        if let Err(e) = file {
            return RunResult::error(self.submission.id, e.to_string());
        }

        let mut file = file.unwrap();
        file.write(self.submission.code.as_bytes());

        let maxium_memory_MB = 512usize;

        let result = std::process::Command::new("docker")
            .arg("run")
            .arg("-i")
            .arg("--cpus=1")
            .arg(format!("--memory={}m", maxium_memory_MB))
            .arg("-v")
            .arg(format!("/tmp/{}:/app/test.cpp", filename))
            .arg("container-cpp")
            .output()
            .expect("failed to execute process");

        println!("exec result {:?}", result);

        return RunResult::output(
            self.submission.id,
            String::from_utf8(result.stdout).unwrap(),
        );
    }
}
