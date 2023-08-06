# -*- coding: utf-8 -*-
from prettytable import PrettyTable

from tikit.tencentcloud.tione.v20211111 import models


def framework_table(framework_response):
    """

    :param framework_response:
    :type framework_response:   :class:`tikit.tencentcloud.tione.v20211111.models.DescribeTrainingFrameworksResponse`
    :return:
    :rtype:
    """
    table = PrettyTable()
    table.field_names = [
        "Framework name",
        "Framework Version",
        "Training mode"
    ]
    for framework in framework_response.FrameworkInfos:
        for framework_version in framework.VersionInfos:
            table.add_row([
                framework.Name,
                "".join(framework_version.Version),
                ", ".join(framework_version.TrainingModes)
            ])
    table.align = 'l'
    return table


def framework_str(self):
    return framework_table(self).get_string()


def framework_html(self):
    return framework_table(self).get_html_string()


def bill_specs_table(bill_specs_response):
    """

    :param bill_specs_response:
    :type bill_specs_response:   :class:`tikit.tencentcloud.tione.v20211111.models.DescribeBillingSpecsResponse`
    :return:
    :rtype:
    """
    table = PrettyTable()
    table.field_names = [
        "Instance type",
        "Describe",
        "USD per hour"
    ]
    for spec in bill_specs_response.Specs:
        table.add_row([
            spec.SpecName,
            spec.SpecAlias,
            spec.SpecId
        ])
    return table


def bill_specs_str(self):
    return bill_specs_table(self).get_string()


def bill_specs_html(self):
    return bill_specs_table(self).get_html_string()


def training_task_table(training_task_response):
    """

    :param training_task_response:
    :type training_task_response:   :class:`tikit.tencentcloud.tione.v20211111.models.DescribeTrainingTasksResponse`
    :return:
    :rtype:
    """
    paid_dict = {
        "PREPAID": "Prepaid",
        "POSTPAID_BY_HOUR": "PostPaid"
    }
    table = PrettyTable()
    table.field_names = [
        "Task ID",
        "Task name",
        "Training framework",
        "Training mode",
        "Pay mode",
        "Tags",
        "Status",
        "Running time",
        "Begin time"
    ]
    for task in training_task_response.TrainingTaskSet:
        if task.RuntimeInSeconds > 86400:
            time_str = "{}day(s){}hour{}minute(s){}second(s)".format(int(task.RuntimeInSeconds / 86400),
                                              int((task.RuntimeInSeconds % 86400) / 3600),
                                              int((task.RuntimeInSeconds % 3600) / 60),
                                              task.RuntimeInSeconds % 60)
        elif task.RuntimeInSeconds > 3600:
            time_str = "{}hour{}minute(s){}second(s)".format(int(task.RuntimeInSeconds / 3600),
                                           int((task.RuntimeInSeconds % 3600) / 60),
                                           task.RuntimeInSeconds % 60)
        else:
            time_str = "{}minute(s){}second(s)".format(int(task.RuntimeInSeconds / 60), task.RuntimeInSeconds % 60)
        if len(task.FrameworkName) > 0:
            framework = "{}:{}".format(task.FrameworkName, task.FrameworkVersion)
        else:
            framework = "CUSTOM"  # TODO
        table.add_row([
            task.Id,
            task.Name,
            framework,
            task.TrainingMode,
            paid_dict[task.ChargeType],
            "\n".join(map(lambda x: "%s:%s" % (x.TagKey, x.TagValue), task.Tags)),
            task.Status,
            time_str,
            task.StartTime
        ])
    return table


def training_task_str(self):
    return training_task_table(self).get_string()


def training_task_html(self):
    return training_task_table(self).get_html_string()


def log_table(log_response):
    """

    :param log_response:
    :type log_response:   :class:`tikit.tencentcloud.tione.v20211111.models.DescribeLogsResponse`
    :return:
    :rtype:
    """
    table = PrettyTable()
    table.field_names = [
        "Log time",
        "Instance name",
        "Log content"
    ]
    for one_log in log_response.Content:
        table.add_row([
            one_log.Timestamp,
            one_log.PodName,
            one_log.Message
        ])
    table.align = 'l'
    return table


def log_str(self):
    return log_table(self).get_string()


def log_html(self):
    return log_table(self).get_html_string()


models.DescribeTrainingFrameworksResponse.__repr__ = framework_str
models.DescribeTrainingFrameworksResponse._repr_html_ = framework_html

models.DescribeBillingSpecsResponse.__repr__ = bill_specs_str
models.DescribeBillingSpecsResponse._repr_html_ = bill_specs_html

models.DescribeTrainingTasksResponse.__repr__ = training_task_str
models.DescribeTrainingTasksResponse._repr_html_ = training_task_html

models.DescribeLogsResponse.__repr__ = log_str
models.DescribeLogsResponse._repr_html_ = log_html
