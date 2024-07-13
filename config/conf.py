CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
CELERY_TIMEZONE = 'Asia/Tehran'
broker_connection_retry_on_startup = True
accept_content = ['json']
task_serializer = 'json'
result_serializer = 'json'
broker_transport_options = {"visibility_timeout": 3600},  # 1 hour
worker_prefetch_multiplier = 1
task_ignore_result = False
task_track_started = True
task_time_limit = 600  # 10 minutes
worker_concurrency = 2
task_always_eager = False
task_eager_propagates = True
task_soft_time_limit = 300  # 5 minutes
task_acks_late = True
worker_max_tasks_per_child = 100
broker_connection_retry = True
result_expires = 3600  # 1 hour
enable_utc = True
beat_sync_every = 10
beat_max_loop_interval = 300  # 5 minutes
broker_heartbeat = 120  # Heartbeat frequency in seconds
broker_pool_limit = 10  # Limit number of active connections to the broker
event_queue_expires = 120  # Events expire after 60 seconds
event_queue_ttl = 120  # Time-to-live for event messages
worker_disable_rate_limits = True  # Disable rate limits for tasks
worker_send_task_events = True  # Send task-related events for monitoring
worker_lost_wait = 10  # Time to wait for worker to reconnect before marking as lost
task_annotations = {
    '*': {'rate_limit': '10/m'}  # Global rate limit for tasks (10 per minute)
}
worker_state_db = 'celery_worker_state'  # Path to worker state database
task_default_delivery_mode = 1  # Delivery mode (1 = transient, 2 = persistent)
result_persistent = True  # Persist results to backend

# Monitoring and security configurations
worker_autoscale = '10,3'  # Autoscale: max 10 workers, min 3 workers
worker_enable_remote_control = True  # Enable remote control for workers
worker_consumer_heartbeat = 60  # Worker consumer heartbeat interval in seconds
task_publish_retry = True  # Retry task publishing on failure
task_publish_retry_policy = {
    'max_retries': 3,  # Maximum number of retries
    'interval_start': 0,  # Start retry interval
    'interval_step': 0.2,  # Incremental interval steps
    'interval_max': 0.5,  # Maximum retry interval
}
worker_redirect_stdouts = True  # Redirect stdout
worker_redirect_stdouts_level = 'INFO'  # Redirect stdout level
result_backend_transport_options = {
    'visibility_timeout': 43200,  # Result backend visibility timeout (12 hours)
}
task_reject_on_worker_lost = True  # Reject task if worker is lost
worker_log_color = True  # Enable colored logging for workers
task_default_rate_limit = '200/m'  # Default rate limit for tasks (200 per minute)
