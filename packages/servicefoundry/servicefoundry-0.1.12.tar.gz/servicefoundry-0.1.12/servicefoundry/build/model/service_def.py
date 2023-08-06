import json

from ..const import SERVICE_TYPE_MAPPING, ADDITIONAL_PACKAGES, COMMAND


class ServiceDef:
    def __init__(self, name, build, deployments):
        self.name = name
        self.build: ServiceBuild = build
        self.deployments = deployments

    def get_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)


class ServiceBuild:
    def __init__(
        self, service_type, service_file, version, build_dir,
            packages, ignore_patterns, port
    ):
        self.type = "ServiceBuild"
        self.service_type = service_type
        self.service_file = service_file
        self.version = version
        self.build_dir = build_dir
        self.packages = packages
        self.ignore_patterns = ignore_patterns
        self.port = port

    def get_requirement_txt(self):
        if not isinstance(self.packages, list):
            return self.packages
        else:
            return None

    def get_packages(self):
        ret_val = []
        ret_val.extend(SERVICE_TYPE_MAPPING[self.service_type][ADDITIONAL_PACKAGES])
        if isinstance(self.packages, list):
            ret_val.extend(self.packages)
        return ret_val

    def get_run_command(self):
        module_name = self.service_file
        if self.service_file.endswith(".py"):
            module_name = module_name.split(".")[0]
        return SERVICE_TYPE_MAPPING[self.service_type][COMMAND](module_name, self.port)


class HealthCheck:
    def __init__(self, endpoint, period_seconds, initial_delay):
        self.endpoint = endpoint
        self.period_seconds = period_seconds
        self.initial_delay = initial_delay


class HttpsService:
    def __init__(
        self,
        namespace,
        port,
        cpu,
        memory,
        cpu_limit,
        memory_limit,
        instances,
        metrics_endpoint,
        env,
        health_check: HealthCheck,
    ):
        self.type = "HttpsService"
        self.namespace = namespace
        self.port = port
        self.cpu = cpu
        self.memory = memory
        self.cpu_limit = cpu_limit
        self.memory_limit = memory_limit
        self.instances = instances
        self.metrics_endpoint = metrics_endpoint
        self.env = env
        self.health_check = health_check
