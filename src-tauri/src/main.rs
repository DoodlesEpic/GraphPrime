#![cfg_attr(
    all(not(debug_assertions), target_os = "windows"),
    windows_subsystem = "windows"
)]

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![calculate])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}

#[tauri::command]
async fn calculate(x: u64) -> Vec<u64> {
    // Define an array of Boolean values, index from 2 to n, initially all set to true.
    let mut is_prime = vec![true; (x + 1) as usize];

    // Sieve of Eratosthenes
    for i in 2..x {
        if is_prime[i as usize] {
            for j in (i * i..=x).step_by(i as usize) {
                is_prime[j as usize] = false;
            }
        }
    }

    // Return all prime numbers in the array
    is_prime
        .iter()
        .enumerate()
        .skip(2)
        .filter(|(_, &is_prime)| is_prime)
        .map(|(i, _)| i as u64)
        .collect()
}
