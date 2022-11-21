const MYSQL_SERVER_URL: &'static str = "mysql://kukudev:rhdqngofk!%40%23@127.0.0.1:20022/kuku_dev";

mod language;
use language::*;
use mysql_async::prelude::*;
use mysql_async::Conn;
use rayon::prelude::*;
use tokio;

#[derive(Debug)]
enum Job {
    CPlusPlus(language::CPlusPlus),
    Java(language::Java),
    Python(language::Python),
    Unknwon(u64),
}
impl Job {
    pub fn run(mut self) -> RunResult {
        let result = match self {
            Job::CPlusPlus(mut c) => c.run(),
            Job::Java(mut j) => j.run(),
            Job::Python(mut p) => p.run(),
            Job::Unknwon(id) => RunResult::error(id, "Unknown language".to_string()),
        };

        println!("--> result {:?}", result);
        return result;
    }
}

fn main() {
    tokio::runtime::Builder::new_multi_thread()
        .enable_all()
        .build()
        .unwrap()
        .block_on(main_loop());
}

async fn main_loop() {
    loop {
        tokio::time::sleep(tokio::time::Duration::from_secs(1)).await;

        let jobs = list_jobs().await;
        println!("--> code_jobs return {:?}", jobs);
        if let Ok(mut jobs) = jobs {
            println!("--> select code_jobs {:?}", jobs);

            if jobs.len() == 0 {
                continue;
            }

            let results: Vec<RunResult> = jobs.par_drain(..).map(|job| job.run()).collect();

            tokio::spawn(update_jobs(results));
        }
    }
}

async fn list_jobs() -> Result<Vec<Job>, Box<dyn std::error::Error>> {
    let pool = mysql_async::Pool::new(MYSQL_SERVER_URL);
    let mut conn = pool.get_conn().await?;

    println!("select code_jobs");

    Ok("select * from code_jobs"
        .with(())
        .map::<(u64, String, String, String, mysql_async::Value), Job, _, &mut Conn>(
            &mut conn,
            |(id, langauge, code, status, status_updated)| {
                let submission = Submission::new(id, langauge, status, code, status_updated);

                match submission.language.as_str() {
                    "c++" => Job::CPlusPlus(language::CPlusPlus::new(submission)),
                    "python" => Job::Python(language::Python::new(submission)),
                    "java" => Job::Java(language::Java::new(submission)),
                    _ => Job::Unknwon(submission.id),
                }
            },
        )
        .await
        .unwrap_or(vec![]))
}

async fn update_jobs(mut results: Vec<RunResult>) {
    loop {
        let pool = mysql_async::Pool::new(MYSQL_SERVER_URL);
        let conn = pool.get_conn().await;

        if conn.is_err() {
            pool.disconnect().await;
            continue;
        }

        let insert_result =
            r"INSERT INTO jobs_result (id, output, error) VALUES (:id, :output, :error)"
                .with(results.drain(..).map(|result| {
                    if result.result.is_ok() {
                        params! {
                            "id" => result.id,
                            "output" => result.result.unwrap(),
                            "error" => "",
                        }
                    } else {
                        params! {
                            "id" => result.id,
                            "output" => result.result.unwrap(),
                            "error" => "",
                        }
                    }
                }))
                .batch(&mut conn.unwrap())
                .await;

        if insert_result.is_ok() {
            pool.disconnect().await;
            break;
        }
    }
}
