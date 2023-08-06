def format_function_id(team_id, function_id):
    if team_id is None:
        return function_id

    if ":" not in function_id:
        function_id = "{}:{}".format(team_id, function_id)

    return function_id


def format_environment_id(team_id, function_id, environment_name):
    function_id = format_function_id(team_id, function_id)

    return "{}:{}".format(function_id, environment_name)


def split_function_id(function_id):
    parts = function_id.split(":")
    team_id = None

    if len(parts) == 1:
        [function_id] = parts
    else:
        [team_id, function_id] = parts

    return team_id, function_id


def split_environment_id(environment_id):
    parts = environment_id.split(":")
    team_id = None

    if len(parts) == 2:
        [function_id, environment_name] = parts
    else:
        [team_id, function_id, environment_name] = parts

    return team_id, function_id, environment_name


def append_cookie(cookie, key, value):
    if key is None or value is None:
        return cookie

    if cookie is None:
        cookie = ""

    cookies = [string.strip() for string in cookie.split(";")]
    cookies = [string for string in cookies if string != ""]
    cookies = [string for string in cookies if not string.startswith("{}=".format(key))]

    cookies.append("{}={}".format(key, value))
    return "; ".join(cookies)
