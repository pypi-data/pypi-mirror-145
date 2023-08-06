import yaml
import re

from servicefoundry.build.model.service_def import ServiceBuild, ServiceDef, HealthCheck, HttpsService


def _get_or_throw(definition, key, error_message):
    if key not in definition:
        raise RuntimeError(error_message)
    return definition[key]


def _get_or_none(definition, key):
    if key not in definition:
        return None
    return definition[key]


def _resolve(variable_name, value):
    if type(value) == str:
        m = re.search("\${(.*)}", value)
        if m and len(m.groups()) == 1:
            variable = m.group(1)
            if variable.startswith("stage."):
                env_variable = variable[6:]
                return variable_name[env_variable]
            elif variable.startswith("secret."):
                return value
            else:
                raise RuntimeError(
                    "Only stage and secret are allowed to be used as variable"
                )
    elif type(value) == dict:
        result = {}
        for key in value.keys():
            result[key] = _resolve(variable_name, value[key])
        return result
    return value


SERVICE_BUILD = "service_build"
HTTPS_SERVICE = "https_service"


class Parser:
    def __init__(self):
        self.valid_builds = {SERVICE_BUILD: self.parse_service_build}
        self.valid_deploy = {HTTPS_SERVICE: self.parse_https_service}

    def parse(self, service_def_file_path):
        with open(service_def_file_path, "r") as stream:
            service_def = yaml.safe_load(stream)

        name = _get_or_throw(
            service_def, "name", "Name not found in service definition."
        )
        build = self.parse_build(
            _get_or_throw(
                service_def, "build", "build not found in service definition."
            )
        )
        envs = self.parse_stages(
            _get_or_throw(service_def, "envs", "envs not found in service definition.")
        )
        deployments = {}
        for env in envs.keys():
            deployments[env] = self.parse_deploy(
                envs[env],
                _get_or_throw(
                    service_def, "deploy", "deploy not found in service definition."
                ),
            )
        return ServiceDef(name=name, build=build, deployments=deployments)

    def parse_build(self, build):
        if len(build.keys()) == 0:
            raise RuntimeError(f"Build is not defined.")
        if len(build.keys()) > 1:
            raise RuntimeError(f"More than one build provided.")
        build_name = list(build.keys())[0]
        if build_name in self.valid_builds:
            return self.valid_builds[build_name](build[build_name])
        raise RuntimeError(
            f"Build can be one of {self.valid_builds.keys()}. Found {build.keys()}"
        )

    def parse_service_build(self, service_auto_build):
        service_type = _get_or_throw(
            service_auto_build,
            "service_type",
            "service_type not found in service_auto_build.",
        )

        service_file = _get_or_throw(
            service_auto_build, "service_file", "service not found in service_auto_build."
        )
        version = _get_or_throw(
            service_auto_build, "version", "version not found in service_auto_build."
        )

        build_dir = _get_or_none(service_auto_build, "build_dir")
        packages = _get_or_none(service_auto_build, "packages")

        ignore_patterns = _get_or_none(service_auto_build, "ignore_patterns")
        port = _get_or_none(service_auto_build, "port")

        return ServiceBuild(
            service_type=service_type,
            service_file=service_file,
            version=version,
            build_dir=build_dir,
            packages=packages,
            ignore_patterns=ignore_patterns,
            port=port,
        )

    def parse_stages(self, stages):
        stage_map = {}
        for key in stages.keys():
            stage_map[key] = self.parse_stage(stages[key])
        return stage_map

    def parse_stage(self, stage):
        variable_map = {}
        for key in stage.keys():
            variable_map[key] = stage[key]
        return variable_map

    def parse_deploy(self, variable_map, deploy):
        if len(deploy.keys()) == 0:
            raise RuntimeError(f"Build is not defined.")
        if len(deploy.keys()) > 1:
            raise RuntimeError(f"More than one build provided.")
        deploy_name = list(deploy.keys())[0]
        if deploy_name in self.valid_deploy:
            return self.valid_deploy[deploy_name](variable_map, deploy[deploy_name])
        raise RuntimeError(
            f"Deploy can be one of {self.valid_deploy.keys()}. Found {deploy.keys()}"
        )

    def parse_https_service(self, variable_map, http_service):
        namespace = _resolve(
            variable_map,
            _get_or_throw(
                http_service, "namespace", "namespace not found in https_service."
            ),
        )
        port = _resolve(
            variable_map,
            _get_or_throw(
                http_service, "port", "namespace not found in https_service."
            ),
        )
        cpu = _resolve(
            variable_map,
            _get_or_throw(http_service, "cpu", "cpu not found in https_service."),
        )
        memory = _resolve(
            variable_map,
            _get_or_throw(http_service, "memory", "memory not found in https_service."),
        )
        cpu_limit = _resolve(
            variable_map,
            _get_or_throw(
                http_service, "cpu_limit", "cpu_limit not found in https_service."
            ),
        )
        memory_limit = _resolve(
            variable_map,
            _get_or_throw(
                http_service, "memory_limit", "memory_limit not found in https_service."
            ),
        )
        instances = _resolve(
            variable_map,
            _get_or_throw(
                http_service, "instances", "instances not found in https_service."
            ),
        )
        metrics_endpoint = _resolve(
            variable_map,
            _get_or_throw(
                http_service,
                "metrics_endpoint",
                "metrics_endpoint not found in https_service.",
            ),
        )
        env = _resolve(
            variable_map,
            _get_or_throw(http_service, "env", "env not found in https_service."),
        )

        health_check = _get_or_throw(
            http_service, "health_check", "health_check not found in https_service."
        )
        health_check = self.parse_health_check(variable_map, health_check)

        return HttpsService(
            namespace=namespace,
            port=port,
            cpu=cpu,
            memory=memory,
            cpu_limit=cpu_limit,
            memory_limit=memory_limit,
            instances=instances,
            metrics_endpoint=metrics_endpoint,
            env=env,
            health_check=health_check,
        )

    def parse_health_check(self, variable_map, health_check):
        endpoint = _resolve(
            variable_map,
            _get_or_throw(
                health_check, "endpoint", "endpoint not found in health_check."
            ),
        )
        period_seconds = _resolve(
            variable_map,
            _get_or_throw(
                health_check,
                "period_seconds",
                "period_seconds not found in health_check.",
            ),
        )
        initial_delay = _resolve(
            variable_map,
            _get_or_throw(
                health_check,
                "initial_delay",
                "initial_delay not found in health_check.",
            ),
        )
        return HealthCheck(
            endpoint=endpoint,
            period_seconds=period_seconds,
            initial_delay=initial_delay,
        )
