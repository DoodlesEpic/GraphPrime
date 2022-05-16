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
    let mut result = vec![2];

    // Only iterate over odd numbers since 2 is the only even prime
    for i in (3..x).step_by(2) {
        if is_prime(i) {
            result.push(i);
        }
    }

    result
}

fn is_prime(x: u64) -> bool {
    for i in 2..x {
        if x % i == 0 {
            return false;
        }
    }
    return true;
}
