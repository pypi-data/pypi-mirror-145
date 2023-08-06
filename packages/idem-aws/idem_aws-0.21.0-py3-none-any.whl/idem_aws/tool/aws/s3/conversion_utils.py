from typing import Any
from typing import Dict


def convert_raw_bucket_notification_to_present(
    hub, raw_resource: Dict[str, Any], bucket_name: str
) -> Dict[str, Any]:
    """
    Convert the s3 bucket notification configurations response to a common format

    Args:
        raw_resource: List of s3 bucket notification configurations
        bucket_name: Name of the bucket on which notification needs to be configured.

    Returns:
        A dictionary of s3 bucket notification configurations
    """
    translated_resource = {}
    raw_resource.pop("ResponseMetadata", None)

    if raw_resource:
        translated_resource["name"] = bucket_name
        translated_resource["resource_id"] = bucket_name + "-notifications"
        translated_resource["notifications"] = raw_resource
    return translated_resource
