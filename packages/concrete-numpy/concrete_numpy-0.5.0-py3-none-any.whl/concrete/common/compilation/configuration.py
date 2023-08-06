"""Module for compilation configuration."""


class CompilationConfiguration:
    """Class that allows the compilation process to be customized."""

    dump_artifacts_on_unexpected_failures: bool
    enable_topological_optimizations: bool
    check_every_input_in_inputset: bool
    treat_warnings_as_errors: bool
    enable_unsafe_features: bool
    random_inputset_samples: int
    use_insecure_key_cache: bool
    auto_parallelize: bool
    loop_parallelize: bool
    dataflow_parallelize: bool

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        dump_artifacts_on_unexpected_failures: bool = True,
        enable_topological_optimizations: bool = True,
        check_every_input_in_inputset: bool = False,
        treat_warnings_as_errors: bool = False,
        enable_unsafe_features: bool = False,
        random_inputset_samples: int = 30,
        use_insecure_key_cache: bool = False,
        auto_parallelize: bool = False,
        loop_parallelize: bool = True,
        dataflow_parallelize: bool = False,
    ):
        self.dump_artifacts_on_unexpected_failures = dump_artifacts_on_unexpected_failures
        self.enable_topological_optimizations = enable_topological_optimizations
        self.check_every_input_in_inputset = check_every_input_in_inputset
        self.treat_warnings_as_errors = treat_warnings_as_errors
        self.enable_unsafe_features = enable_unsafe_features
        self.random_inputset_samples = random_inputset_samples
        self.use_insecure_key_cache = use_insecure_key_cache
        self.auto_parallelize = auto_parallelize
        self.loop_parallelize = loop_parallelize
        self.dataflow_parallelize = dataflow_parallelize

    # pylint: enable=too-many-arguments

    def __eq__(self, other) -> bool:
        return isinstance(other, CompilationConfiguration) and self.__dict__ == other.__dict__
