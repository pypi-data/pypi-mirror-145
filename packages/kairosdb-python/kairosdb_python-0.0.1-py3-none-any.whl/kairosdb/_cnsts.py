API_PREFIX = "/api/v1"
VERSION_API = f"{API_PREFIX}/version"
HEALTH_STATUS_API = f"{API_PREFIX}/health/status"
HEALTH_CHECK_API = f"{API_PREFIX}/health/check"
QUERY_API = f"{API_PREFIX}/datapoints/query"
ADD_DATA_API = f"{API_PREFIX}/datapoints"
DELETE_DATA_API = f"{API_PREFIX}/datapoints/delete"
DELETE_METRIC_API = f"{API_PREFIX}/metric/"  # add metric name as path parameter
FEATURES_API = f"{API_PREFIX}/features"
METRIC_NAMES_API = f"{API_PREFIX}/metricnames"
METADATA_API = ""
QUERY_TAGS_API = f"{API_PREFIX}/datapoints/query/tags"
ROLL_UPS = f"{API_PREFIX}/rollups"

SUCCESS_CODES = (200, 201, 202, 203, 204,)
