"""
Monitoring and Observability Configuration

Comprehensive observability configuration including metrics, tracing,
logging, and health checks.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class MonitoringSettings(BaseModel):
    """
    Monitoring and observability configuration for comprehensive
    application insights and performance tracking.
    """

    # Metrics Configuration (Prometheus)
    metrics_enabled: bool = Field(default=True, description="Enable Prometheus metrics")
    metrics_path: str = Field(default="/metrics", description="Metrics endpoint path")
    metrics_port: int = Field(default=9090, description="Metrics server port")
    metrics_namespace: str = Field(default="backend_app", description="Metrics namespace")
    metrics_subsystem: str = Field(default="api", description="Metrics subsystem")

    # Custom Metrics
    collect_request_metrics: bool = Field(
        default=True, description="Collect HTTP request metrics"
    )
    collect_database_metrics: bool = Field(
        default=True, description="Collect database metrics"
    )
    collect_cache_metrics: bool = Field(default=True, description="Collect cache metrics")
    collect_business_metrics: bool = Field(
        default=True, description="Collect business-specific metrics"
    )

    # Distributed Tracing (OpenTelemetry)
    tracing_enabled: bool = Field(default=True, description="Enable distributed tracing")
    tracing_service_name: str = Field(
        default="modern-backend", description="Service name for tracing"
    )
    tracing_service_version: str = Field(
        default="0.1.0", description="Service version for tracing"
    )

    # Jaeger Configuration
    jaeger_enabled: bool = Field(default=False, description="Enable Jaeger exporter")
    jaeger_agent_host: str = Field(default="localhost", description="Jaeger agent host")
    jaeger_agent_port: int = Field(default=6831, description="Jaeger agent port")
    jaeger_collector_endpoint: str | None = Field(
        default=None, description="Jaeger collector endpoint"
    )

    # Zipkin Configuration
    zipkin_enabled: bool = Field(default=False, description="Enable Zipkin exporter")
    zipkin_endpoint: str = Field(
        default="http://localhost:9411/api/v2/spans", description="Zipkin endpoint"
    )

    # OTLP Configuration
    otlp_enabled: bool = Field(default=False, description="Enable OTLP exporter")
    otlp_endpoint: str = Field(
        default="http://localhost:4317", description="OTLP collector endpoint"
    )
    otlp_headers: dict[str, str] = Field(
        default_factory=dict, description="OTLP headers"
    )

    # Sampling Configuration
    trace_sample_rate: float = Field(
        default=1.0, description="Trace sampling rate (0.0-1.0)"
    )
    span_attribute_value_length_limit: int = Field(
        default=1024, description="Max span attribute value length"
    )
    span_attribute_count_limit: int = Field(
        default=128, description="Max span attribute count"
    )

    # Logging Configuration
    structured_logging: bool = Field(default=True, description="Enable structured logging")
    log_correlation_id: bool = Field(
        default=True, description="Include correlation ID in logs"
    )
    log_request_id: bool = Field(default=True, description="Include request ID in logs")
    log_user_id: bool = Field(default=True, description="Include user ID in logs")

    # Log Levels by Component
    default_log_level: str = Field(default="INFO", description="Default log level")
    database_log_level: str = Field(default="WARNING", description="Database log level")
    http_client_log_level: str = Field(
        default="WARNING", description="HTTP client log level"
    )
    security_log_level: str = Field(default="INFO", description="Security log level")

    # Performance Monitoring
    slow_request_threshold: float = Field(
        default=2.0, description="Slow request threshold (seconds)"
    )
    slow_query_threshold: float = Field(
        default=1.0, description="Slow query threshold (seconds)"
    )
    memory_profiling_enabled: bool = Field(
        default=False, description="Enable memory profiling"
    )
    cpu_profiling_enabled: bool = Field(default=False, description="Enable CPU profiling")

    # Health Checks
    health_check_enabled: bool = Field(default=True, description="Enable health checks")
    health_check_path: str = Field(default="/health", description="Health check endpoint")
    health_check_interval: int = Field(
        default=30, description="Health check interval (seconds)"
    )

    # Health Check Components
    check_database_health: bool = Field(
        default=True, description="Check database connectivity"
    )
    check_redis_health: bool = Field(default=True, description="Check Redis connectivity")
    check_external_apis_health: bool = Field(
        default=True, description="Check external API connectivity"
    )
    check_disk_usage: bool = Field(default=True, description="Check disk usage")
    check_memory_usage: bool = Field(default=True, description="Check memory usage")

    # Health Check Thresholds
    max_response_time: float = Field(
        default=5.0, description="Max acceptable response time (seconds)"
    )
    max_disk_usage_percent: float = Field(
        default=80.0, description="Max disk usage percentage"
    )
    max_memory_usage_percent: float = Field(
        default=80.0, description="Max memory usage percentage"
    )

    # Alerting Configuration
    alerting_enabled: bool = Field(default=False, description="Enable alerting")
    alert_webhook_url: str | None = Field(
        default=None, description="Webhook URL for alerts"
    )
    slack_webhook_url: str | None = Field(
        default=None, description="Slack webhook for alerts"
    )
    email_alerts_enabled: bool = Field(default=False, description="Enable email alerts")
    alert_email_recipients: list[str] = Field(
        default_factory=list, description="Alert email recipients"
    )

    # Error Tracking
    sentry_enabled: bool = Field(default=False, description="Enable Sentry error tracking")
    sentry_dsn: str | None = Field(default=None, description="Sentry DSN")
    sentry_environment: str | None = Field(
        default=None, description="Sentry environment name"
    )
    sentry_sample_rate: float = Field(
        default=1.0, description="Sentry sample rate (0.0-1.0)"
    )

    # Request/Response Logging
    log_requests: bool = Field(default=True, description="Log HTTP requests")
    log_responses: bool = Field(default=False, description="Log HTTP responses")
    log_request_body: bool = Field(default=False, description="Log request body")
    log_response_body: bool = Field(default=False, description="Log response body")
    max_log_body_size: int = Field(
        default=1024, description="Max request/response body size to log"
    )

    # Sensitive Data Protection
    mask_sensitive_data: bool = Field(
        default=True, description="Mask sensitive data in logs"
    )
    sensitive_fields: list[str] = Field(
        default=[
            "password", "token", "secret", "key", "authorization",
            "x-api-key", "cookie", "credit_card", "ssn"
        ],
        description="Fields to mask in logs"
    )

    @property
    def is_tracing_configured(self) -> bool:
        """Check if any tracing exporter is configured."""
        return (
            self.tracing_enabled and (
                self.jaeger_enabled or
                self.zipkin_enabled or
                self.otlp_enabled
            )
        )

    @property
    def is_alerting_configured(self) -> bool:
        """Check if alerting is properly configured."""
        return (
            self.alerting_enabled and (
                self.alert_webhook_url is not None or
                self.slack_webhook_url is not None or
                (self.email_alerts_enabled and self.alert_email_recipients)
            )
        )

    def get_trace_config(self) -> dict:
        """Get tracing configuration for OpenTelemetry."""
        return {
            "service_name": self.tracing_service_name,
            "service_version": self.tracing_service_version,
            "sample_rate": self.trace_sample_rate,
            "span_limits": {
                "attribute_value_length_limit": self.span_attribute_value_length_limit,
                "attribute_count_limit": self.span_attribute_count_limit,
            }
        }

    def get_health_check_config(self) -> dict:
        """Get health check configuration."""
        return {
            "enabled": self.health_check_enabled,
            "path": self.health_check_path,
            "interval": self.health_check_interval,
            "checks": {
                "database": self.check_database_health,
                "redis": self.check_redis_health,
                "external_apis": self.check_external_apis_health,
                "disk": self.check_disk_usage,
                "memory": self.check_memory_usage,
            },
            "thresholds": {
                "response_time": self.max_response_time,
                "disk_usage": self.max_disk_usage_percent,
                "memory_usage": self.max_memory_usage_percent,
            }
        }