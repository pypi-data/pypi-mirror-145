from collections import OrderedDict
from typing import Any
from typing import Dict


async def convert_raw_key_to_present(
    hub, ctx, raw_resource: Dict[str, Any]
) -> Dict[str, Any]:
    describe_parameters = OrderedDict(
        {
            "KeyId": "resource_id",
            "KeyArn": "arn",
            "Arn": "arn",
            "KeyState": "key_state",
            "Description": "description",
            "KeyUsage": "key_usage",
            "KeySpec": "key_spec",
            "MultiRegion": "multi_region",
            "Policy": "policy",
            "Tags": "tags",
        }
    )

    translated_resource = {}
    for parameter_raw, parameter_present in describe_parameters.items():
        if parameter_raw in raw_resource:
            translated_resource[parameter_present] = raw_resource.get(parameter_raw)

    # Get key tags
    # For tag operations key_id is used and not resource_i
    key_tags = await hub.exec.boto3.client.kms.list_resource_tags(
        ctx, KeyId=translated_resource["resource_id"]
    )
    if key_tags and key_tags["result"] is True:
        translated_resource["tags"] = key_tags["ret"].get("Tags", [])

    # Get key policy
    key_policy = await hub.exec.boto3.client.kms.get_key_policy(
        ctx, KeyId=translated_resource["resource_id"], PolicyName="default"
    )
    if (
        key_policy
        and key_policy["result"] is True
        and key_policy["ret"].get("Policy", None)
    ):
        translated_resource[
            "policy"
        ] = hub.tool.aws.state_comparison_utils.standardise_json(
            key_policy["ret"].get("Policy")
        )

    # raw_resource may contains the details already, in this case,
    # skip describe_key call
    if translated_resource.get("key_state", None) is None:
        key_details = await hub.exec.boto3.client.kms.describe_key(
            ctx, KeyId=translated_resource["resource_id"]
        )
        if key_details and key_details["result"] is True:
            resource = key_details["ret"].get("KeyMetadata", {})
            for parameter_raw, parameter_present in describe_parameters.items():
                if parameter_raw in resource:
                    translated_resource[parameter_present] = resource.get(parameter_raw)

    return translated_resource


def convert_raw_key_alias_to_present(
    hub, raw_resource: Dict[str, Any]
) -> Dict[str, Any]:

    # Arn is not used for present but required for arg binding
    resource_parameters = OrderedDict(
        {
            "AliasArn": "arn",
            "TargetKeyId": "target_key_id",
        }
    )
    # AliasName is the unique identifier for KMS Alias, so it is set as resource_id
    translated_resource = {"resource_id": raw_resource.get("AliasName")}
    for parameter_raw, parameter_present in resource_parameters.items():
        if parameter_raw in raw_resource:
            translated_resource[parameter_present] = raw_resource.get(parameter_raw)

    return translated_resource
