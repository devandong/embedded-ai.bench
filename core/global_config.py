#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import sys
import unittest

sys.path.append("..")
from utils.log import LoggerCreator  # noqa

log_enable_debug = False
logger_creator = LoggerCreator(log_enable_debug)
logger = logger_creator.create_logger()


def create_config(framework_name):
    benchmark_platform = ["android-armv7", "android-armv8"]
    config = dict()
    if framework_name == "tnn":
        config["work_dir"] = "./{}".format(framework_name)
        config["model_repo"] = "https://gitee.com/yuens/tnn-models.git"
        # complete model version during `prepare_models`
        config["model_repo_version"] = -1
        config["model_repo_version_extra"] = -1
        config["model_repo_branch"] = -1
        config["model_repo_commit_id"] = -1
        config["device_work_dir"] = "/data/local/tmp/ai-performance/{}".format(
            framework_name
        )
        # complete framework version
        config["framework_repo_branch"] = -1
        config["framework_repo_commit_id"] = -1
        config["framework_name"] = framework_name
        config["benchmark_platform"] = benchmark_platform
        for pidx in range(len(benchmark_platform)):
            platform = benchmark_platform[pidx]
            config[platform] = dict()
            config[platform][
                "shared_lib"
            ] = "./tnn/scripts/build{}/libTNN.so".format(  # noqa
                32 if "v7" in platform else 64
            )
            config[platform][
                "benchmark_bin"
            ] = "./tnn/scripts/build{}/test/TNNTest".format(
                32 if "v7" in platform else 64
            )
        config["repeats"] = 100
        config["warmup"] = 20
        config["support_backend"] = ["ARM", "OPENCL"]
        config["cpu_thread_num"] = [1, 2, 4]
        # power_mode: "big_cores" # "little_cores", "no_bind"
        config["power_mode"] = "big_cores"
        config["benchmark_cmd_pattern"] = (
            'adb -s {serial_num} shell "export LD_LIBRARY_PATH={device_work_dir}; {'  # noqa
            "device_benchmark_bin} -mt {model_type} -mp {model_dir} -dt {backend} -ic {"  # noqa
            'repeats} -wc {warmup} -th {thread_num} -dl {bind_cpu_idx}" '
        )
    else:
        logger.info("Unsupported framework_name: {}".format(framework_name))
        exit(1)
    return config


class TestGlobalConfig(unittest.TestCase):
    def setUp(self):
        logger.info(
            "{} {}".format(
                self.__class__.__name__, sys._getframe().f_code.co_name  # noqa
            )  # noqa
        )

    def tearDown(self):
        logger.info(
            "{} {}".format(
                self.__class__.__name__, sys._getframe().f_code.co_name  # noqa
            )  # noqa
        )

    def test_config(self):
        tnn_config = create_config("tnn")
        logger.info("tnn_config:\n{}".format(tnn_config))
        self.assertNotEqual(tnn_config, dict())


if __name__ == "__main__":
    unittest.main()
