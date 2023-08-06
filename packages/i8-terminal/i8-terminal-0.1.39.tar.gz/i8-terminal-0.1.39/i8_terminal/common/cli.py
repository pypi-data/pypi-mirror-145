from typing import Any, Dict, Optional


def get_click_command_path(ctx: Any, parsed_options_dict: Optional[Dict[str, str]] = None) -> str:
    cm_path = f"i8 {' '.join(ctx.command_path.split(' ')[1:])}"
    params = ctx.params
    args = []
    options = {}
    for p in ctx.command.params:
        if p.param_type_name == "argument":
            args.append(params[p.name])
        elif p.param_type_name == "option" and params[p.name] is not None:
            options[f"--{p.name}"] = params[p.name] if type(params[p.name]) != bool else None

    if parsed_options_dict:
        options = {**options, **parsed_options_dict}
    return f"{cm_path} {' '.join([f'{k} {val}' if val else k for (k, val) in options.items()])} {''.join(args)}"
