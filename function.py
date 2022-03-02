

def update_tags_str(tags_string, tags_to_add_list=[], tags_to_remove_list=[]):
    if not tags_to_add_list and not tags_to_remove_list:
        return tags_string
    
    tag_list = tags_string.split(",")

    # add tags
    for tag in tags_to_add_list:
        if tag.lower() in tag_list:
            tag_list.remove(tag.lower())
            tag_list.append(tag.upper())
        else:
            tag_list.append(tag)

    # remove tags
    for tag in tags_to_remove_list:
        if tag in tag_list:
            tag_list.remove(tag)

    tags_string = ",".join(tag_list)

    return tags_string

"""
Test functionality: 

update_tags_str("acid wash, berry, BIN6, abc", ["tag1", "tag2"], ["berry", "tag2"])

"""