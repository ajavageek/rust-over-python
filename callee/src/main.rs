use axum::routing::post;
use axum::{response::IntoResponse, Json};
use num::Complex;
use serde::{Deserialize, Serialize};

#[tokio::main]
async fn main() {
    let app = axum::Router::new()
        .route("/add", post(add))
        .route("/sub", post(sub))
        .route("/mul", post(mul));
    axum::Server::bind(&"0.0.0.0:3000".parse().unwrap())
        .serve(app.into_make_service())
        .await
        .unwrap()
}

async fn add(Json(payload): Json<Input>) -> impl IntoResponse {
    Json(Output {
        result: payload.a + payload.b,
    })
}

async fn sub(Json(payload): Json<Input>) -> impl IntoResponse {
    Json(Output {
        result: payload.a - payload.b,
    })
}

async fn mul(Json(payload): Json<Input>) -> impl IntoResponse {
    Json(Output {
        result: payload.a * payload.b,
    })
}

#[derive(Deserialize)]
struct Input {
    a: Complex<f64>,
    b: Complex<f64>,
}

#[derive(Serialize)]
struct Output {
    result: Complex<f64>,
}
