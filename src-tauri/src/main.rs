// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use tauri::{Manager, WindowEvent};
use log::{info, error};

// Learn more about Tauri commands at https://tauri.app/develop/calling-rust/
#[tauri::command]
fn greet(name: &str) -> String {
    info!("Greeting user: {}", name);
    format!("Hello, {}! Welcome to AxieStudio Desktop!", name)
}

#[tauri::command]
async fn close_splashscreen(window: tauri::Window) {
    info!("Closing splashscreen");
    // Close splashscreen
    if let Some(splashscreen) = window.get_webview_window("splashscreen") {
        if let Err(e) = splashscreen.close() {
            error!("Failed to close splashscreen: {}", e);
        }
    }
    // Show main window
    if let Some(main) = window.get_webview_window("main") {
        if let Err(e) = main.show() {
            error!("Failed to show main window: {}", e);
        }
    }
}

#[tauri::command]
async fn get_app_version() -> String {
    env!("CARGO_PKG_VERSION").to_string()
}

#[tauri::command]
async fn check_for_updates(app: tauri::AppHandle) -> Result<bool, String> {
    info!("Checking for updates");
    // This would integrate with the updater plugin
    // For now, return false (no updates available)
    Ok(false)
}

fn main() {
    // Initialize logger
    env_logger::init();

    info!("Starting AxieStudio Desktop Application");

    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .plugin(tauri_plugin_dialog::init())
        .plugin(tauri_plugin_fs::init())
        .plugin(tauri_plugin_process::init())
        .plugin(tauri_plugin_updater::Builder::new().build())
        .plugin(tauri_plugin_window_state::Builder::default().build())
        .invoke_handler(tauri::generate_handler![
            greet,
            close_splashscreen,
            get_app_version,
            check_for_updates
        ])
        .on_window_event(|window, event| {
            match event {
                WindowEvent::CloseRequested { .. } => {
                    info!("Window close requested");
                }
                WindowEvent::Focused(focused) => {
                    info!("Window focus changed: {}", focused);
                }
                _ => {}
            }
        })
        .setup(|app| {
            info!("Application setup complete");

            // Set up any initial configuration here
            let main_window = app.get_webview_window("main").unwrap();

            // Configure window properties
            #[cfg(debug_assertions)]
            {
                main_window.open_devtools();
            }

            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
