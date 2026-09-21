#![cfg_attr(
    all(not(debug_assertions), target_os = "windows"),
    windows_subsystem = "windows"
)]

fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_clipboard_manager::init())
        .invoke_handler(tauri::generate_handler![calculate])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}

#[tauri::command]
async fn calculate(x: u64) -> Vec<u64> {
    if x < 2 {
        return Vec::new();
    }

    let sieve = primal::Sieve::new(x as usize);
    // The sieve may include primes beyond the requested limit.
    sieve
        .primes_from(2)
        .map(|p| p as u64)
        .take_while(|&p| p <= x)
        .collect()
}

#[cfg(test)]
mod tests {
    use super::calculate;

    #[test]
    fn calculates_small_sequences_and_boundaries() {
        for (limit, expected) in [
            (0, vec![]),
            (1, vec![]),
            (2, vec![2]),
            (3, vec![2, 3]),
            (4, vec![2, 3]),
            (5, vec![2, 3, 5]),
            (6, vec![2, 3, 5]),
            (7, vec![2, 3, 5, 7]),
            (8, vec![2, 3, 5, 7]),
            (30, vec![2, 3, 5, 7, 11, 13, 17, 19, 23, 29]),
        ] {
            assert_eq!(tauri::async_runtime::block_on(calculate(limit)), expected);
        }
    }

    #[test]
    fn matches_trial_division_for_small_limits() {
        for limit in 0..=1_000 {
            let expected: Vec<u64> = (2..=limit)
                .filter(|&n| (2..).take_while(|&d| d * d <= n).all(|d| n % d != 0))
                .collect();
            assert_eq!(
                tauri::async_runtime::block_on(calculate(limit)),
                expected,
                "limit {limit}"
            );
        }
    }

    #[test]
    fn calculates_scientific_chart_sequences() {
        let primes = tauri::async_runtime::block_on(calculate(100_000));
        assert_eq!(primes.len(), 9_592);
        assert_eq!(primes.last(), Some(&99_991));
        assert!(primes.windows(2).all(|pair| pair[0] < pair[1]));
    }
}
