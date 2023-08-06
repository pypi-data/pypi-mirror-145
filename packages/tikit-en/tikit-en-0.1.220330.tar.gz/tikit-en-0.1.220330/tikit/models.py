# -*- coding: utf-8 -*-
from tikit.tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException

IMAGE_TYPES = ["SYSTEM", "CCR", "TCR"]


class ResourceConfigInfo:
    """Resource configuration

    """

    def __init__(self, charge_type, instance_type=None, instance_num=None, cpu=None, memory=None, gpu_type=None,
                 gpu=None):
        r"""
        :param instance_type: Instance type, eg: TI.S.MEDIUM.POST. Use "describe_postpaid_training_price" to get the list
        :type instance_type: str
        :param instance_num: Instance number
        :type instance_num: int
        :param cpu: Number of cpu，1000=1 core
        :type cpu: int
        :param memory: Memory value in MB
        :type memory: int
        :param gpu_type: Type of GPU
        :type gpu_type: str
        :param gpu: gpu数
        :type gpu: int
        """
        self.ChargeType = charge_type
        self.InstanceNum = instance_num
        self.Cpu = cpu
        self.Memory = memory
        self.GpuType = gpu_type
        self.Gpu = gpu
        self.InstanceType = instance_type

    @staticmethod
    def new_postpaid(instance_type, instance_num):
        """Get the resource configuration in postpaid mode

        :param instance_type:   Instance type, eg: TI.S.MEDIUM.POST. Use "describe_postpaid_training_price" to get the list
        :type instance_type:    str
        :param instance_num:    Instance number
        :type instance_num:     int
        :return:
        :rtype:
        """
        return ResourceConfigInfo(charge_type="POSTPAID_BY_HOUR", instance_type=instance_type,
                                  instance_num=instance_num)

    # @staticmethod
    # def new_prepaid(cpu, memory, gpu=0, gpu_type=None):
    #     """Get the resource configuration in prepaid mode
    #
    #     :param cpu:     CPU value(core)
    #     :type cpu:      float
    #     :param memory:  Memory value in GB
    #     :type memory:   float
    #     :param gpu_type: Type of GPU
    #     :type gpu_type: str
    #     :param gpu:     Number of GPU
    #     :type gpu:      float
    #     :return:
    #     :rtype:
    #     """
    #     cpu = int(cpu * 1000)
    #     memory = int(memory * 1024)
    #     gpu = int(gpu * 100)
    #     return ResourceConfigInfo(charge_type="PREPAID", cpu=cpu, memory=memory, gpu=gpu,
    #                               gpu_type=gpu_type)


class FrameworkInfo:

    def __init__(self, name, training_mode, framework_version=None, image_type=None, image_url=None,
                 registry_region=None, registry_id=None):
        self.Name = name
        self.TrainingMode = training_mode

        self.FrameworkVersion = framework_version

        self.ImageType = image_type
        self.ImageUrl = image_url
        self.RegistryRegion = registry_region
        self.RegistryId = registry_id

    @staticmethod
    def new_custom(training_mode, image_type, image_url, registry_region=None, registry_id=None):
        """Customize training framework configuration

        :param training_mode:   Training mode. Use "describe_training_frameworks" to get list
        :type training_mode:    str
        :param image_type:      Image type in Tencent Container Registry. eg: CCR
        :type image_type:       str
        :param image_url:       Image url in Tencent Container Registry
        :type image_url:        str
        :param registry_region: Region of Tencent Container Registry
        :type registry_region:  str
        :param registry_id:     ID of Tencent Container Registry
        :type registry_id:      str
        :return:
        :rtype:
        """
        return FrameworkInfo(name="CUSTOM",
                             training_mode=training_mode,
                             image_type=image_type,
                             image_url=image_url,
                             registry_region=registry_region,
                             registry_id=registry_id)

    @staticmethod
    def new_system_framework(framework_name, framework_version, training_mode):
        """Built-in training framework of the system

        :param framework_name:      Framework name. Use "describe_training_frameworks" to get list
        :type framework_name:       str
        :param framework_version:   Framework version. Use "describe_training_frameworks" to get list
        :type framework_version:    str
        :param training_mode:       Training mode. Use "describe_training_frameworks" to get list
        :type training_mode:        str
        :return:
        :rtype:
        """
        return FrameworkInfo(name=framework_name,
                             framework_version=framework_version,
                             training_mode=training_mode)


class TrainingDataConfig:
    def __init__(self):
        self.DataSource = None
        self.DataConfigDict = None  # Deprecated
        self.TargetPath = None
        self.CosStr = None
        self.DatasetId = None
        self.CfsId = None
        self.CfsPath = None
        self.HdfsId = None
        self.HdfsPath = None

    @staticmethod
    def new_mount_cos(cos_str, target_path):
        """Create a new training dataset configuration of COS type.

        :param cos_str:      COS info. Format:  <bucket>/<cos path>/
        :type cos_str: str
        :param  target_path:  target path to mount
        :type target_path: str
        :return:
        :rtype:
        """
        ret = TrainingDataConfig()
        ret.TargetPath = target_path
        ret.DataSource = "COS"
        ret.CosStr = cos_str
        return ret

    @staticmethod
    def new_dataset_mount(dataset_id, target_path):
        """Create a new training dataset configuration of dataset type.

        :param dataset_id:  dataset id
        :type dataset_id: str
        :param  target_path:  target path to mount
        :type target_path: str
        :return:
        :rtype:
        """
        ret = TrainingDataConfig()
        ret.TargetPath = target_path
        ret.DataSource = "DATASET"
        ret.DatasetId = dataset_id
        return ret

    @staticmethod
    def new_mount_cfs(cfs_id, source_path, target_path):
        """Create a new training dataset configuration of CFS type.

        :param cfs_id:      ID of CFS
        :type cfs_id: str
        :param  source_path: source path of CFS
        :type source_path: str
        :param  target_path: target path to mount
        :type target_path: str
        :return:
        :rtype:
        """
        ret = TrainingDataConfig()
        ret.TargetPath = target_path
        ret.DataSource = "CFS"
        ret.CfsId = cfs_id
        ret.CfsPath = source_path
        return ret

    @staticmethod
    def new_mount_hdfs(hdfs_id, source_path, target_path):
        """Create a new training dataset configuration of hdfs type.

        :param hdfs_id:      ID of EMR with HDFS
        :type hdfs_id: str
        :param  source_path: source path of HDFS
        :type source_path: str
        :param  target_path: target path to mount
        :type target_path: str
        :return:
        :rtype:
        """
        ret = TrainingDataConfig()
        ret.TargetPath = target_path
        ret.DataSource = "HDFS"
        ret.HdfsId = hdfs_id
        ret.HdfsPath = source_path
        return ret

    @staticmethod
    def new_dataset(id_target_dict):
        """Create a new training dataset configuration of dataset type. --Deprecated!

        :param id_target_dict:  Dataset info. Format: dataset ID -> target path
        :type id_target_dict:   dict
        :return:
        :rtype:
        """
        ret = TrainingDataConfig()
        ret.DataSource = "DATASET"
        ret.DataConfigDict = id_target_dict
        return ret

    @staticmethod
    def new_cos_data(cos_str_target_dict):
        """Create a new training dataset configuration of COS type. --Deprecated!

        :param cos_str_target_dict:     Dataset info. Format:  <bucket>/<cos path>/ -> target path
        :type cos_str_target_dict:      dict
        :return:
        :rtype:
        """
        ret = TrainingDataConfig()
        ret.DataSource = "COS"
        ret.DataConfigDict = cos_str_target_dict
        return ret


class ReasoningEnvironment:
    def __init__(self, source, image_key=None, image_type=None, image_url=None, registry_region=None, registry_id=None):
        self.Source = source
        self.ImageKey = image_key
        self.ImageType = image_type
        self.ImageUrl = image_url
        self.RegistryRegion = registry_region
        self.RegistryId = registry_id

    @staticmethod
    def new_system_environment(image_key):
        """Built-in running environment of the platform

        :param image_key:   Image key。Use "describe_training_frameworks" to get image key list
        :type image_key:    str
        :return:
        :rtype:
        """
        return ReasoningEnvironment("SYSTEM", image_key)

    @staticmethod
    def new_custom_environment(image_type, image_url, registry_region=None, registry_id=None):
        """Custom inference running environment

        :param image_type:      Image type in Tencent Container Registry. eg: CCR
        :type image_type:       str
        :param image_url:       Image url in Tencent Container Registry
        :type image_url:        str
        :param registry_region: Region of Tencent Container Registry
        :type registry_region:  str
        :param registry_id:     ID of Tencent Container Registry
        :type registry_id:      str
        :return:
        :rtype:
        """
        if image_type not in IMAGE_TYPES:
            raise TencentCloudSDKException(message='image_type not must in {}'.format(IMAGE_TYPES))
        return ReasoningEnvironment("CUSTOM",
                                    image_type=image_type,
                                    image_url=image_url,
                                    registry_region=registry_region,
                                    registry_id=registry_id)
