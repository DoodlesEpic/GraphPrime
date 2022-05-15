#![cfg_attr(
    all(not(debug_assertions), target_os = "windows"),
    windows_subsystem = "windows"
)]

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![is_prime])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}

#[tauri::command]
fn is_prime(x: u64) -> bool {
    for i in 2..x {
        if x % i == 0 {
            return false;
        }
    }
    return true;
}
