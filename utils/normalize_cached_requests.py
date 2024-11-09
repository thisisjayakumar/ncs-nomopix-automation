import json


def normalize_cached_json(cached_json_str):
    try:
        if cached_json_str.startswith('"') and cached_json_str.endswith('"'):
            cached_json_str = cached_json_str[1:-1]
        cached_json_str = cached_json_str.replace('\\"', '"')
        normalized_json = json.loads(cached_json_str)

        return normalized_json

    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON: {str(e)}")
    except Exception as e:
        raise Exception(f"An error occurred while normalizing JSON: {str(e)}")