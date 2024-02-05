def get_content_until(tagname: str, head_tag, include_head=True, join_str="\n") -> str:
    tag_list = []
    current = head_tag

    if include_head is True:
        tag_list.append(current)

    current = current.find_next_sibling()

    while current != None and current.name != tagname:
        tag_list.append(current)
        current = current.find_next_sibling()

    return f"{join_str}".join([tag.text for tag in tag_list])
