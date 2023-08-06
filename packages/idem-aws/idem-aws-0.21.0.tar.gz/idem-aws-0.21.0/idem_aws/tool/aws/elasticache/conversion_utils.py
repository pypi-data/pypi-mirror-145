from collections import OrderedDict
from typing import Any
from typing import Dict

"""
Util functions to convert raw resource state from AWS Elasticache to present input format.
"""


async def convert_raw_elasticache_subnet_to_present(
    hub, ctx, raw_resource: Dict[str, Any], idem_resource_name: str = None
) -> Dict[str, Any]:
    resource_id = raw_resource.get("CacheSubnetGroupName")
    resource_parameters = OrderedDict(
        {
            "CacheSubnetGroupDescription": "cache_subnet_group_description",
        }
    )
    resource_translated = {"name": idem_resource_name, "resource_id": resource_id}
    for parameter_raw, parameter_present in resource_parameters.items():
        if parameter_raw in raw_resource:
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)

    if raw_resource.get("Subnets"):
        subnet_ids_list = []
        for subnets in raw_resource.get("Subnets"):
            if "SubnetIdentifier" in subnets:
                subnet_ids_list.append(subnets.get("SubnetIdentifier"))
        resource_translated["subnet_ids"] = subnet_ids_list
    if raw_resource.get("ARN"):
        tags = await hub.exec.boto3.client.elasticache.list_tags_for_resource(
            ctx, ResourceName=raw_resource.get("ARN")
        )
        if tags["result"]:
            if tags["ret"]["TagList"]:
                resource_translated["tags"] = tags["ret"]["TagList"]
    return resource_translated
