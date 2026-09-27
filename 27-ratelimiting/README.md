# FastAPI Rate Limiting ⚡

A clean, production-ready implementation of IP-based rate limiting in **FastAPI** using **SlowAPI**.

---

## ✨ Features

- **Client IP Tracking**: Automatically identifies clients using `slowapi.util.get_remote_address`.
- **Granular Route Limits**: Simple decorator-based rate limiting (e.g., `@limiter.limit("5/minute")`).
- **Custom 429 Responses**: Returns structured JSON error payloads when limits are exceeded.

---

## 🚀 Quickstart

### 1. Install Dependencies

```bash
pip install fastapi uvicorn slowapi
```

### 2. Run the Application

```bash
uvicorn main:app --reload
```

Interactive documentation is available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

---

## 📡 API Reference

### Rate-Limited Route

```http
GET /data
```

- **Limit**: `5 requests / minute` per client IP.

#### Sample Request

```bash
curl -i http://127.0.0.1:8000/data
```

#### Success (`200 OK`)

```json
{
  "message": "Rate limiter api"
}
```

#### Rate Limit Exceeded (`429 Too Many Requests`)

```json
{
  "message": "Too many requests. Please try again later."
}
```

---

## 🔍 How It Works

1. **Limiter Initialization**: `Limiter(key_func=get_remote_address)` binds rate-tracking to the client's IP.
2. **State Attachment**: Assigned to `app.state.limiter` for application lifecycle integration.
3. **Exception Handler**: Catches `RateLimitExceeded` and serves standard HTTP 429 JSON responses.
4. **Endpoint Decorator**: `@limiter.limit("5/minute")` throttles subsequent calls after threshold.

---

## 📂 Project Structure

```text
├── main.py        # App initialization, rate limiter & routes
└── README.md      # Documentation
```

---

## 📜 License

MIT
