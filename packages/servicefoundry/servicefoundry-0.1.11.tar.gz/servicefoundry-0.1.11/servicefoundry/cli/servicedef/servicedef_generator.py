import yaml
from jinja2 import Template

from servicefoundry.build.util import create_file_from_content, read_text


def generate_service_def(service_name, build_type, build_dict, stage_params, deploy_type):
    template = Template(read_text("servicefoundry.j2", name=__name__))
    return template.render(
        service_name=service_name,
        build_type=build_type,
        build_dict=build_dict,
        deployment_type=deploy_type,
        stage_params=stage_params,
    )


class CustomDumper(yaml.SafeDumper):
    def write_line_break(self, data=None):
        super().write_line_break(data)

        if len(self.indents) == 1:
            super().write_line_break()


def generate_service_def_yml(service_def_obj):
    return yaml.dump(service_def_obj,  Dumper=CustomDumper, default_flow_style=False, sort_keys=False)
