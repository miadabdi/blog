FROM python:3.13.5-slim-bookworm AS builder

# Set working directory
WORKDIR /code

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --prefix=/install --no-compile --no-cache-dir -r requirements.txt


FROM python:3.13.5-slim-bookworm

# Create a non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set working directory
WORKDIR /code

# Copy only built Python packages
COPY --from=builder /install /usr/local

# Copy application code
COPY . .

# Change ownership of the code directory to appuser
RUN chown -R appuser:appuser /code

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 80

# Set environment variables
ENV PYTHON_ENV=production
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Health check (optional but recommended)
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:80/health || exit 1

# Use exec form for better signal handling
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]