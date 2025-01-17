from app import app

# Add timeout configurations
timeout = 120  # 2 minutes
keepalive = 5

if __name__ == "__main__":
    app.run() 
