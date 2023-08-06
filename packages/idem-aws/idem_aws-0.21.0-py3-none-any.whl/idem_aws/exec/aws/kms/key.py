import copy
from typing import Any
from typing import Dict
from typing import List


async def update_key_tags(
    hub,
    ctx,
    key_id: str,
    old_tags: List[Dict[str, Any]],
    new_tags: List[Dict[str, Any]],
):
    """

    Args:
        hub:
        ctx:
        key_id: aws kms key id
        old_tags: list of old tags
        new_tags: list of new tags

    Returns:
        {"result": True|False, "comment": Tuple, "ret": "Tags after update"}

    """
    result = dict(comment=(), result=True, ret=None)

    tags_to_add = list()
    old_tags_map = {tag.get("TagKey"): tag for tag in old_tags}
    tags_result = copy.deepcopy(old_tags_map)
    for tag in new_tags:
        if tag.get("TagKey") in old_tags_map:
            # Make sure the key and value are the same before deleting
            if tag.get("TagValue") == old_tags_map.get(tag.get("TagKey")).get(
                "KeyValue"
            ):
                del old_tags_map[tag.get("TagKey")]
            else:
                tags_to_add.append(tag)
        else:
            tags_to_add.append(tag)
    tags_to_remove = [tag.get("TagKey") for tag in old_tags_map.values()]
    if tags_to_remove and not ctx.get("test", False):
        delete_ret = await hub.exec.boto3.client.kms.untag_resource(
            ctx, KeyId=key_id, TagKeys=tags_to_remove
        )
        if not delete_ret["result"]:
            result["comment"] = delete_ret["comment"]
            result["result"] = False
            return result
    if tags_to_add and not ctx.get("test", False):
        add_ret = await hub.exec.boto3.client.kms.tag_resource(
            ctx, KeyId=key_id, Tags=tags_to_add
        )
        if not add_ret["result"]:
            result["comment"] = add_ret["comment"]
            result["result"] = False
            return result
    for key in tags_to_remove:
        tags_result.pop(key)
    result["ret"] = {"tags": list(tags_result.values()) + tags_to_add}
    if ctx.get("test", False):
        result["comment"] = (
            f"Would update tags: Add [{tags_to_add}] Remove [{tags_to_remove}]",
        )
    else:
        result["comment"] = (
            f"Updated tags: Added [{tags_to_add}] Removed [{tags_to_remove}]",
        )
    return result
