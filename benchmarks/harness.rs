// Injected into temporary copies of BOTH revisions by scripts/benchmark.py.
// This calls the actual application command, including its async runtime.
use std::{
    hint::black_box,
    time::{Duration, Instant},
};

#[test]
#[ignore = "run through scripts/benchmark.py for paired performance measurements"]
fn sample() {
    let limit: u64 = std::env::var("GRAPHPRIME_BENCH_LIMIT")
        .unwrap()
        .parse()
        .unwrap();
    let operation = std::env::var("GRAPHPRIME_BENCH_OPERATION").unwrap();
    let duration = Duration::from_millis(
        std::env::var("GRAPHPRIME_BENCH_MS")
            .unwrap()
            .parse()
            .unwrap(),
    );
    let primes = tauri::async_runtime::block_on(super::calculate(limit));
    let (count, last) = match limit {
        1_000 => (168, 997),
        100_000 => (9_592, 99_991),
        1_000_000 => (78_498, 999_983),
        10_000_000 => (664_579, 9_999_991),
        _ => panic!("unsupported benchmark limit"),
    };
    assert_eq!(primes.len(), count);
    assert_eq!(primes.last(), Some(&last));
    assert!(primes.windows(2).all(|pair| pair[0] < pair[1]));
    let run = || match operation.as_str() {
        "calculate" => {
            black_box(tauri::async_runtime::block_on(super::calculate(black_box(
                limit,
            ))));
        }
        "serialize" => {
            black_box(serde_json::to_vec(black_box(&primes)).unwrap());
        }
        _ => panic!("unsupported benchmark operation"),
    };
    // Warm allocator, code and data caches before measuring; exclude startup.
    let warmup = Instant::now();
    while warmup.elapsed() < Duration::from_millis(100) {
        run();
    }
    let start = Instant::now();
    let mut iterations = 0_u64;
    while start.elapsed() < duration {
        run();
        iterations += 1;
    }
    let ns_per_iteration = start.elapsed().as_nanos() as f64 / iterations as f64;
    println!(
        "GRAPHPRIME_BENCH {}",
        serde_json::json!({
            "ns_per_iteration": ns_per_iteration,
            "iterations": iterations,
        })
    );
}
