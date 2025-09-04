// Tauri API configuration for Axie Studio backend integration
use tauri::command;
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct ApiConfig {
    pub backend_url: String,
    pub timeout: u64,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct HealthResponse {
    pub status: String,
}

#[command]
pub async fn get_backend_url() -> Result<String, String> {
    // Return the production backend URL for Tauri builds
    Ok("https://flow.axiestudio.se".to_string())
}

#[command]
pub async fn check_backend_health() -> Result<HealthResponse, String> {
    let client = reqwest::Client::new();
    
    match client
        .get("https://flow.axiestudio.se/health")
        .timeout(std::time::Duration::from_secs(10))
        .send()
        .await
    {
        Ok(response) => {
            if response.status().is_success() {
                match response.json::<HealthResponse>().await {
                    Ok(health) => Ok(health),
                    Err(e) => Err(format!("Failed to parse health response: {}", e)),
                }
            } else {
                Err(format!("Backend health check failed with status: {}", response.status()))
            }
        }
        Err(e) => Err(format!("Failed to connect to backend: {}", e)),
    }
}

#[command]
pub async fn get_api_config() -> Result<ApiConfig, String> {
    Ok(ApiConfig {
        backend_url: "https://flow.axiestudio.se".to_string(),
        timeout: 30000, // 30 seconds
    })
}
