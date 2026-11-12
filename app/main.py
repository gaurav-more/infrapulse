from fastapi import FastAPI

app = FastAPI(
    title = "InfraPulse API",
    description = "Infrastructure Monitoring and Automation Platform",
    version = "0.1.0"
)

@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status" : "healthy",
        "service" : "infrapulse"
    }

