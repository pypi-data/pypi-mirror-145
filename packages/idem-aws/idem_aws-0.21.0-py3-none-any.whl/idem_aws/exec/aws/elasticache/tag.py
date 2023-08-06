import copy
from typing import Any
from typing import Dict
from typing import List


async def update_tags(
    hub,
    ctx,
    resource_arn: str,
    old_tags: List[Dict[str, Any]],
    new_tags: List[Dict[str, Any]],
):
    """

    Args:
        hub:
        ctx:
        resource_arn: aws elasticache arn
        old_tags: List of existing tags
        new_tags: List of new tags

    Returns:
        {"result": True|False, "comment": "A message", "ret": None}

    """

    result = dict(comment="", result=True, ret=None)

    old_tags_map = {tag.get("Key"): tag.get("Value") for tag in old_tags or []}
    new_tags_map = {tag.get("Key"): tag.get("Value") for tag in new_tags or []}
    tags_result = copy.deepcopy(old_tags_map)

    if old_tags_map == new_tags_map:
        result["comment"] = "All tags are updated!"
        return result

    tags_to_add = []
    tags_to_delete = []

    for key, value in new_tags_map.items():
        if (key in old_tags_map and old_tags_map.get(key) != new_tags_map.get(key)) or (
            key not in old_tags_map
        ):
            tags_to_add.append({"Key": key, "Value": value})

    for key in old_tags_map:
        if key not in new_tags_map:
            tags_to_delete.append(key)
    try:
        if not ctx.get("test", False) and tags_to_delete:
            delete_tag_resp = (
                await hub.exec.boto3.client.elasticache.remove_tags_from_resource(
                    ctx, ResourceName=resource_arn, TagKeys=tags_to_delete
                )
            )
            if not delete_tag_resp["result"]:
                hub.log.debug(f"Could not delete tags {tags_to_delete}")
                result["comment"] = delete_tag_resp["comment"]
                result["result"] = False
                return result

            hub.log.debug(f"Deleted tags {tags_to_delete}")
        [tags_result.pop(key, None) for key in tags_to_delete]
    except hub.tool.boto3.exception.ClientError as e:
        hub.log.debug(f"Error while deleting tags {tags_to_delete}")
        result["comment"] = f"{e.__class__.__name__}: {e}"
        result["result"] = False

    try:
        if not ctx.get("test", False) and tags_to_add:
            create_tag_resp = (
                await hub.exec.boto3.client.elasticache.add_tags_to_resource(
                    ctx, ResourceName=resource_arn, Tags=tags_to_add
                )
            )
            if not create_tag_resp["result"]:
                hub.log.debug(f"Could not create tags {tags_to_add}")
                result["comment"] = create_tag_resp["comment"]
                result["result"] = False
                return result

            hub.log.debug(f"Created tags {tags_to_add}")
    except hub.tool.boto3.exception.ClientError as e:
        hub.log.debug(f"Error while creating tags {tags_to_add}")
        result["comment"] = f"{e.__class__.__name__}: {e}"
        result["result"] = False

    result["ret"] = {"tags": list(tags_result.values()) + tags_to_add}
    result["comment"] = (f"Update tags: Add [{tags_to_add}] Remove [{tags_to_delete}]",)
    result["result"] = True
    return result
