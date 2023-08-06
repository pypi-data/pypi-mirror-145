# -*- coding: utf-8 -*-
from prettytable import PrettyTable

from tikit.tencentcloud.tione.v20211111 import models


def dataset_table(dataset_response):
    """

    :param dataset_response:
    :type dataset_response:   :class:`tikit.tencentcloud.tione.v20211111.models.DescribeDatasetsResponse`
    :return:
    :rtype:
    """
    type_dict = {
        "TYPE_DATASET_TEXT": "TEXT",
        "TYPE_DATASET_TABLE": "TABLE",
        "TYPE_DATASET_IMAGE": "IMAGE",
        "TYPE_DATASET_OTHER": "OTHER"
    }
    unit_dict = {
        "TYPE_DATASET_TEXT": "rows",
        "TYPE_DATASET_TABLE": "rows",
        "TYPE_DATASET_IMAGE": "",
        "TYPE_DATASET_OTHER": ""
    }
    table = PrettyTable()
    table.field_names = [
        "ID",
        "Name",
        "Version",
        "Type",
        "Tags",
        "Status",
        "Number",
        "Source path on COS",
        "Label storage path",
        "Labeling task name",
        "Create time"
    ]
    for dataset in dataset_response.DatasetGroups:
        table.add_row([
            dataset.DatasetId,
            dataset.DatasetName,
            dataset.DatasetVersion,
            type_dict[dataset.DatasetType],
            "\n".join(map(lambda x: "%s:%s" % (x.TagKey, x.TagValue), dataset.DatasetTags)),
            dataset.DatasetStatus,
            "{}{}".format(dataset.FileNum, unit_dict[dataset.DatasetType]),
            dataset.StorageDataPath,
            dataset.StorageLabelPath,
            dataset.DatasetAnnotationTaskName,
            dataset.CreateTime
        ])
    return table


def dataset_str(self):
    return dataset_table(self).get_string()


def dataset_html(self):
    return dataset_table(self).get_html_string()


def detail_structured_table(detail_structured):
    """

    :param detail_structured:
    :type detail_structured:   :class:`tikit.tencentcloud.tione.v20211111.models.DescribeDatasetDetailStructuredResponse`
    :return:
    :rtype:
    """
    table = PrettyTable()
    table.field_names = detail_structured.ColumnNames
    for row_item in detail_structured.RowItems:
        row = []
        for column in table.field_names:
            field_value = ""
            for name_value in row_item.Values:
                if name_value.Name == column:
                    field_value = name_value.Value
                    break
            row.append(field_value)
        table.add_row(row)
    return table


def detail_structured_str(self):
    return detail_structured_table(self).get_string()


def detail_structured_html(self):
    return detail_structured_table(self).get_html_string()


def detail_unstructured_table(detail_unstructured):
    """

    :param detail_unstructured:
    :type detail_unstructured:   :class:`tikit.tencentcloud.tione.v20211111.models.DescribeDatasetDetailStructuredResponse`
    :return:
    :rtype:
    """
    table = PrettyTable()
    table.field_names = [
        "Total Count",
        "Unlabeled Count",
        "Labeled Count",
    ]
    table.add_row([
        detail_unstructured.FilterTotalCount,
        detail_unstructured.NonAnnotatedTotalCount,
        detail_unstructured.AnnotatedTotalCount
    ])
    return table


def detail_unstructured_str(self):
    return detail_unstructured_table(self).get_string()


def detail_unstructured_html(self):
    return detail_unstructured_table(self).get_html_string()


models.DescribeDatasetsResponse.__repr__ = dataset_str
models.DescribeDatasetsResponse._repr_html_ = dataset_html

models.DescribeDatasetDetailStructuredResponse.__repr__ = detail_structured_str
models.DescribeDatasetDetailStructuredResponse._repr_html_ = detail_structured_html

models.DescribeDatasetDetailUnstructuredResponse.__repr__ = detail_unstructured_str
models.DescribeDatasetDetailUnstructuredResponse._repr_html_ = detail_unstructured_html
