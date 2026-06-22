FROM python:3.11-slim

WORKDIR /app

# Optimize container layers by installing requirements directly
RUN pip install --no-cache-dir \
    fastapi==0.121.2 \
    uvicorn==0.38.0 \
    streamlit==1.56.0 \
    pydantic==2.11.7 \
    google-genai==1.50.1 \
    mcp==1.28.0 \
    fastmcp==3.4.0 \
    httpx==0.28.1 \
    httpx-sse==0.4.3

# Copy the application source code files into the container space
COPY . .

# Expose generic network layers
EXPOSE 8501

# Hand execution management over to our custom manager script
CMD ["python", "launcher.py"]
