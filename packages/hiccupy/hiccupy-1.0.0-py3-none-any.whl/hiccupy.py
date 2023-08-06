def insert_href(element: list, href: str = "?id={curie}", depth: int = 0) -> list:
    """Add 'href' attributes to each 'a' tag that has a 'resource', but not an 'href'.
    Return the updated list.

    :param element: hiccup-style list to add 'href' attributes to
    :param href: pattern for href where the {curie} is replaced with 'resource'
    :param depth: list depth of current element
    :return copy of element with added 'href'
    """
    render_element = element.copy()
    if not isinstance(render_element, list):
        raise TypeError(f"Element is not a list: {element}")
    if len(render_element) == 0:
        raise ValueError("Element is an empty list")
    tag = render_element.pop(0)
    if not isinstance(tag, str):
        raise ValueError(f"Tag '{tag}' at loc {depth} is not a string")
    output = [tag]

    if len(render_element) > 0 and isinstance(render_element[0], dict):
        attrs = render_element.pop(0)
        if tag == "a" and "href" not in attrs and "resource" in attrs:
            attrs["href"] = href.format(curie=attrs["resource"])
        output.append(attrs)

    if len(render_element) > 0:
        for child in render_element:
            if isinstance(child, str):
                output.append(child)
            elif isinstance(child, list):
                output.append(insert_href(child, href=href, depth=depth + 1))
            else:
                raise TypeError(f"Bad type for '{tag}' child '{child}' at loc {depth + 1}")
    return output


def render(element: list, depth: int = 0) -> str:
    """Render hiccup-style HTML vector as HTML.

    :param element: hiccup-style list
    :param depth: list depth of current element
    :return HTML string
    """
    render_element = element.copy()
    indent = "  " * depth
    if not isinstance(render_element, list):
        raise Exception(f"Element is not a list: {element}")
    if len(render_element) == 0:
        raise Exception("Element is an empty list")
    tag = render_element.pop(0)
    if not isinstance(tag, str):
        raise Exception(f"Tag '{tag}' at loc {depth} is not a string")
    output = f"{indent}<{tag}"

    if len(render_element) > 0 and isinstance(render_element[0], dict):
        attrs = render_element.pop(0)
        for key, value in attrs.items():
            if key in ["checked"]:
                if value:
                    output += f" {key}"
            else:
                output += f' {key}="{value}"'

    if tag in ["meta", "link", "path"]:
        output += "/>"
        return output
    output += ">"
    spacing = ""
    if len(render_element) > 0:
        for child in render_element:
            if isinstance(child, str):
                output += child
            elif isinstance(child, list):
                output += "\n" + render(child, depth=depth + 1)
                spacing = f"\n{indent}"
            else:
                raise Exception(f"Bad type for '{tag}' child '{child}' at loc {depth + 1}")
    output += f"{spacing}</{tag}>"
    return output
