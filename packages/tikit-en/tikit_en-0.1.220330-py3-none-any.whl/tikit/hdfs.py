# -*- coding: utf-8 -*-
import os

from hdfs import Client as HdfsClient


def upload_to_hdfs(local_path, hdfs_url, hdfs_path):
    """Upload Local files to HDFS

    :param local_path:  Local path
    :type local_path:   str
    :param hdfs_url:    WebHDFS address, such as: http://10.0.3.16:4008
    :type hdfs_url:     str
    :param hdfs_path:   Result path on HDFS
    :type hdfs_path:    str
    :return:            Result path on HDFS
    :rtype:             str
    """
    hdfs_client = HdfsClient(hdfs_url)
    # 上传文件到一个不存在的目录（斜杠结尾）的时候，hdfs库会把目录当成最终文件
    if os.path.isfile(local_path) and hdfs_path.endswith("/"):
        hdfs_path = os.path.join(hdfs_path, os.path.basename(local_path))
    return hdfs_client.upload(hdfs_path, local_path)


def download_from_hdfs(hdfs_url, hdfs_path, local_path):
    """Download files from HDFS to a local path

    :param hdfs_url:    WebHDFS address, such as: http://10.0.3.16:4008
    :type hdfs_url:     str
    :param hdfs_path:   Path on HDFS
    :type hdfs_path:    str
    :param local_path:  Local result path
    :type local_path:   str
    :return:            Local result path
    :rtype:             str
    """
    hdfs_client = HdfsClient(hdfs_url)
    path_info = hdfs_client.status(hdfs_path)
    # 下载文件到一个不存在的目录（斜杠结尾）的时候，hdfs库会把目录当成最终文件
    if path_info["type"] == "FILE" and local_path.endswith("/"):
        local_path = os.path.join(local_path, os.path.basename(hdfs_path))
    # 创建目录
    local_dir = os.path.dirname(local_path)
    if local_dir != "" and not os.path.exists(local_dir):
        os.makedirs(local_dir)
    return hdfs_client.download(hdfs_path, local_path)
