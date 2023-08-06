import copy
import json
import jsonschema
import pandas as pd

# from https://www.speedscope.app/file-format-schema.json
speedscope_schema = json.loads(
    """{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "definitions": {
        "CloseFrameEvent": {
            "properties": {
                "at": {
                    "title": "at",
                    "type": "number"
                },
                "frame": {
                    "title": "frame",
                    "type": "number"
                },
                "type": {
                    "enum": [
                        "C"
                    ],
                    "title": "type",
                    "type": "string"
                }
            },
            "required": [
                "at",
                "frame",
                "type"
            ],
            "title": "CloseFrameEvent",
            "type": "object"
        },
        "FileFormat.EventType": {
            "enum": [
                "C",
                "O"
            ],
            "title": "FileFormat.EventType",
            "type": "string"
        },
        "FileFormat.EventedProfile": {
            "properties": {
                "endValue": {
                    "title": "endValue",
                    "type": "number"
                },
                "events": {
                    "items": {
                        "anyOf": [
                            {
                                "$ref": "#/definitions/OpenFrameEvent"
                            },
                            {
                                "$ref": "#/definitions/CloseFrameEvent"
                            }
                        ]
                    },
                    "title": "events",
                    "type": "array"
                },
                "name": {
                    "title": "name",
                    "type": "string"
                },
                "startValue": {
                    "title": "startValue",
                    "type": "number"
                },
                "type": {
                    "enum": [
                        "evented"
                    ],
                    "title": "type",
                    "type": "string"
                },
                "unit": {
                    "$ref": "#/definitions/FileFormat.ValueUnit",
                    "title": "unit"
                }
            },
            "required": [
                "endValue",
                "events",
                "name",
                "startValue",
                "type",
                "unit"
            ],
            "title": "FileFormat.EventedProfile",
            "type": "object"
        },
        "FileFormat.File": {
            "properties": {
                "$schema": {
                    "enum": [
                        "https://www.speedscope.app/file-format-schema.json"
                    ],
                    "title": "$schema",
                    "type": "string"
                },
                "activeProfileIndex": {
                    "title": "activeProfileIndex",
                    "type": ["number", "null"]
                },
                "exporter": {
                    "title": "exporter",
                    "type": "string"
                },
                "name": {
                    "title": "name",
                    "type": "string"
                },
                "profiles": {
                    "items": {
                        "anyOf": [
                            {
                                "$ref": "#/definitions/FileFormat.EventedProfile"
                            },
                            {
                                "$ref": "#/definitions/FileFormat.SampledProfile"
                            }
                        ]
                    },
                    "title": "profiles",
                    "type": "array"
                },
                "shared": {
                    "properties": {
                        "frames": {
                            "items": {
                                "$ref": "#/definitions/FileFormat.Frame"
                            },
                            "title": "frames",
                            "type": "array"
                        }
                    },
                    "required": [
                        "frames"
                    ],
                    "title": "shared",
                    "type": "object"
                }
            },
            "required": [
                "$schema",
                "profiles",
                "shared"
            ],
            "title": "FileFormat.File",
            "type": "object"
        },
        "FileFormat.Frame": {
            "properties": {
                "col": {
                    "title": "col",
                    "type": ["number", "null"]
                },
                "file": {
                    "title": "file",
                    "type": "string"
                },
                "line": {
                    "title": "line",
                    "type": "number"
                },
                "name": {
                    "title": "name",
                    "type": "string"
                }
            },
            "required": [
                "name"
            ],
            "title": "FileFormat.Frame",
            "type": "object"
        },
        "FileFormat.IProfile": {
            "properties": {
                "type": {
                    "$ref": "#/definitions/FileFormat.ProfileType",
                    "title": "type"
                }
            },
            "required": [
                "type"
            ],
            "title": "FileFormat.IProfile",
            "type": "object"
        },
        "FileFormat.Profile": {
            "anyOf": [
                {
                    "$ref": "#/definitions/FileFormat.EventedProfile"
                },
                {
                    "$ref": "#/definitions/FileFormat.SampledProfile"
                }
            ]
        },
        "FileFormat.ProfileType": {
            "enum": [
                "evented",
                "sampled"
            ],
            "title": "FileFormat.ProfileType",
            "type": "string"
        },
        "FileFormat.SampledProfile": {
            "properties": {
                "endValue": {
                    "title": "endValue",
                    "type": "number"
                },
                "name": {
                    "title": "name",
                    "type": "string"
                },
                "samples": {
                    "items": {
                        "items": {
                            "type": "number"
                        },
                        "type": "array"
                    },
                    "title": "samples",
                    "type": "array"
                },
                "startValue": {
                    "title": "startValue",
                    "type": "number"
                },
                "type": {
                    "enum": [
                        "sampled"
                    ],
                    "title": "type",
                    "type": "string"
                },
                "unit": {
                    "$ref": "#/definitions/FileFormat.ValueUnit",
                    "title": "unit"
                },
                "weights": {
                    "items": {
                        "type": "number"
                    },
                    "title": "weights",
                    "type": "array"
                }
            },
            "required": [
                "endValue",
                "name",
                "samples",
                "startValue",
                "type",
                "unit",
                "weights"
            ],
            "title": "FileFormat.SampledProfile",
            "type": "object"
        },
        "FileFormat.ValueUnit": {
            "enum": [
                "bytes",
                "microseconds",
                "milliseconds",
                "nanoseconds",
                "none",
                "seconds"
            ],
            "title": "FileFormat.ValueUnit",
            "type": "string"
        },
        "IEvent": {
            "properties": {
                "at": {
                    "title": "at",
                    "type": "number"
                },
                "type": {
                    "$ref": "#/definitions/FileFormat.EventType",
                    "title": "type"
                }
            },
            "required": [
                "at",
                "type"
            ],
            "title": "IEvent",
            "type": "object"
        },
        "OpenFrameEvent": {
            "properties": {
                "at": {
                    "title": "at",
                    "type": "number"
                },
                "frame": {
                    "title": "frame",
                    "type": "number"
                },
                "type": {
                    "enum": [
                        "O"
                    ],
                    "title": "type",
                    "type": "string"
                }
            },
            "required": [
                "at",
                "frame",
                "type"
            ],
            "title": "OpenFrameEvent",
            "type": "object"
        },
        "SampledStack": {
            "items": {
                "type": "number"
            },
            "type": "array"
        }
    },
    "$ref": "#/definitions/FileFormat.File"
}
"""
)


def validate_speedscope_json(json_data):
    try:
        jsonschema.validate(instance=json_data, schema=speedscope_schema)
    except jsonschema.exceptions.ValidationError as err:
        raise err
        return False
    return True


def get_cpu_by_function(json_data, granularity="functions"):
    frames = json_data["shared"]["frames"]
    profile = json_data["profiles"][0]
    samples = profile["samples"]
    intermediate_dict = {}
    for stack in samples:
        stack_l = []
        last_n = len(stack)
        for n, frame_pos in enumerate(stack, 1):
            frame = frames[frame_pos]
            name = frame["name"]
            file = ""
            if "file" in frame:
                file = frame["file"]
            line = ""
            if "line" in frame:
                line = frame["line"]
            full_fname = "{} {}".format(name, file)
            if granularity == "lines" and line != "":
                full_fname = "{}:{} {}".format(name, line, file)
            full_fname = full_fname.strip(" ")
            if full_fname not in intermediate_dict:
                intermediate_dict[full_fname] = {"flat": 0, "cum": 0}

            if full_fname not in stack_l:
                intermediate_dict[full_fname]["cum"] = (
                    intermediate_dict[full_fname]["cum"] + 1
                )
                stack_l.append(full_fname)
            if n == last_n:
                intermediate_dict[full_fname]["flat"] = (
                    intermediate_dict[full_fname]["flat"] + 1
                )
        al = []
        for k, v in intermediate_dict.items():
            flat_p = float(v["flat"]) / len(samples) * 100.0
            cum_p = float(v["cum"]) / len(samples) * 100.0
            al.append((k, flat_p, cum_p))
    df = pd.DataFrame(al, columns=["symbol", "flat%", "cum%"])
    df = df.sort_values(by=["flat%"], ascending=False)
    df["flat%"] = df["flat%"].map("{:,.2f}".format)
    df["cum%"] = df["cum%"].map("{:,.2f}".format)
    js = json.loads(df.to_json(orient="records"))

    res = {"data": js, "totalRows": len(al), "totalPages": 1, "labels": []}
    return res


def get_node(name, function, value=0):
    node = {"n": name, "f": function, "v": value, "c": {}}
    return node


def touch_node(parent_node, key, name, function, value=0):
    if key not in parent_node["c"]:
        parent_node["c"][key] = get_node(name, function, value)
    return parent_node["c"][key]


def get_flamegraph(json_data):
    root_node = get_node("root", "root", 0)
    frames = json_data["shared"]["frames"]
    profile = json_data["profiles"][0]
    samples = profile["samples"]
    for stack in samples:
        previous_node = root_node
        last_n = len(stack)
        for n, frame_pos in enumerate(stack, 1):
            frame = frames[frame_pos]
            name = frame["name"]
            file = ""
            if "file" in frame:
                file = frame["file"]
            line = ""
            if "line" in frame:
                line = frame["line"]
            full_fname = "{} {}".format(name, file)
            if line != "":
                full_fname = "{}:{} {}".format(name, line, file)
                # name = "{}:{}".format(name, line)
            full_fname = full_fname.strip(" ")
            name = name.strip(" ")
            current_node = touch_node(previous_node, full_fname, full_fname, full_fname)
            if n == last_n:
                current_node["v"] = current_node["v"] + 1
            previous_node = current_node

    res = flatten_tree(root_node)
    print(res)
    return res


def flatten_tree(root_node):
    res = copy.deepcopy(root_node)
    res["c"] = []
    for v in root_node["c"].values():
        # print("flattening {}".format(v["f"]))
        res["c"].append(flatten_tree(v))
    return res
