import json

import markdown
import os
from bs4 import BeautifulSoup

EXPOSE_TYPES = {
    "text": "string",
    "numeric": "integer",
    "binary": "boolean",
    # TODO: с указанием типа внутри
    "list": "array",
    "enum": "enum",
    "composite": "composite",
}

# TODO: Specific composites
SPECIFIC_COMPOSITES = {
    "light": "light",
    "switch": "switch",
    "fan": "fan",
    "cover": "cover",
    "lock": "lock",
    "climate": "climate"
}


def main():
    devices_path = "./mds/devices"
    dirs = [d for d in os.listdir(devices_path) if os.path.isfile(os.path.join(devices_path, d))]

    for dir in dirs:
        with open(os.path.join(devices_path, dir)) as file:
            md = markdown.markdown(file.read())
            soup = BeautifulSoup(md)
            name = soup.find("h1").text
            exposes = soup.find("h2", text="Exposes").find_all_next("h3")
            scheme = {
                "title": name,
                "type": "object",
                "properties": {}
            }

            for expose in exposes:
                expose_parts = expose.text.split(" ")
                e_name = expose_parts[0].lower()

                # TODO: Если тип относится к SPECIFIC_COMPOSITES
                if len(expose_parts) == 1:
                    if e_name == "light":
                        scheme["properties"][e_name] = __get_light_scheme()

                e_type = expose_parts[1].replace("(", "").replace(")", "").split(",")[0]

                # if type_s not in EXPOSE_TYPES and exp_s[0].lower() not in SPECIFIC_COMPOSITES:
                if e_type in EXPOSE_TYPES:
                    if e_type == "enum":
                        code_els = expose.find_next_sibling("p").find_all("code")

                        try:
                            start_idx = [idx for idx, el in enumerate(code_els) if __is_expose_values_start_el(el)][0]
                        except IndexError:
                            with open('broken.txt', 'w') as b_file:
                                b_file.write(dir + "\n")
                                continue

                        end_idx = \
                            [idx for idx, el in enumerate(code_els) if __is_expose_values_end_el(el, idx, start_idx)][0]
                        values = [el.text for el in code_els[start_idx:end_idx + 1]]
                        scheme["properties"][e_name] = {
                            "type": "string",
                            "enum": values
                        }
                        continue

                    scheme["properties"][e_name] = {
                        "type": EXPOSE_TYPES[e_type]
                    }

            with open(f"./schemes/{name.lower().replace(' ', '_').replace('-', '_').replace('/', '_')}.json", "w") as s_file:
                s_file.write(json.dumps(scheme))
                print(f"Write {name}")


def __is_expose_values_start_el(el, ) -> bool:
    try:
        el.previous_sibling.text.index("The possible values are:")
        return True
    except ValueError:
        return False


def __is_expose_values_end_el(el, idx: int, start_idx: int) -> bool:
    return el.next_sibling == "." and idx >= start_idx


def __get_light_scheme() -> dict:
    return {
        "type": "object",
        "properties": {
            "state": {"type": "boolean"},
            "brightness": {"type": "integer"},
            "color_temp": {"type": "integer"},
            "color_xy": {
                "type": "object",
                "properties": {
                    "x": {"type": "integer"},
                    "y": {"type": "integer"}
                }
            },
            "color_hs": {
                "type": "object",
                "properties": {
                    "hue": {"type": "integer"},
                    "saturation": {"type": "integer"}
                }
            }
        }
    }


if __name__ == '__main__':
    main()
