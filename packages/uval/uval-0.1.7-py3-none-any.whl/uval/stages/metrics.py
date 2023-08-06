# -*- coding: utf-8 -*-
"""This module provides stages that can compute metrics like overlaps between
groundtruth and detections, or simply count detections per bag.
"""
import math
import os
import pickle
import sys
from multiprocessing import Pool
from typing import Any, Dict, List, Tuple, Union

import jinja2  # type: ignore
import matplotlib  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
import numpy as np
import pandas as pd  # type: ignore
from rich.progress import track

from uval.stages.stage import uval_stage  # type: ignore
from uval.stages.stage_data import SupportedDatasetSpecificationData
from uval.utils.log import logger

matplotlib.use("Agg")


class DetectionEntry:
    """Any detection entry wether it is from GT or detections will be converted in this form."""

    def __init__(
        self, volume_id: str, class_name: str, confidence_score: float, roi_start: Tuple[int], roi_shape: Tuple[int]
    ):
        self.volume_id = volume_id
        self.class_name = class_name
        self.confidence_score = confidence_score
        self.roi_start = roi_start
        self.roi_shape = roi_shape


class Metrics:
    """This class implements all the evaluation metrics."""

    def __init__(self, dataset: SupportedDatasetSpecificationData, metrics_settings, output_settings):
        self.dataset = dataset

        self.data = None
        self.iou_threshold = metrics_settings.IOU_THRESHOLD

        self.template_file = "template.html"
        if len(metrics_settings.IOU_RANGE) == 3:
            a, b, c = metrics_settings.IOU_RANGE
            self.iou_range = np.linspace(a, b, int(np.round((b - a) / c)) + 1, endpoint=True).tolist()
            self.iou_range = [round(iou, 2) for iou in self.iou_range]
            self.template_file = "template_range.html"
        else:
            self.iou_range = None
        self.confidence_threshold = metrics_settings.CONFIDENCE_THRESHOLD
        self.output_path = output_settings.PATH

        self.title = output_settings.TITLE or self.output_path.split("/")[-1]

        self.report_file = output_settings.REPORT_FILE
        self.metrics_file = output_settings.METRICS_FILE
        self.max_workers = metrics_settings.MAX_PROCESSES
        self.templates_path = output_settings.TEMPLATES_PATH
        self.ap_method = metrics_settings.AP_METHOD
        self.factor = metrics_settings.FACTOR

    def evaluate(self):
        metrics_output = dict()
        basics = self.basic_metric(iou_threshold=self.iou_threshold, confidence_threshold=self.confidence_threshold)
        ap_metrics = self.get_average_precision(basics, method=self.ap_method)
        fscore_metrics = self.get_fscore(ap_metrics)
        metrics_output["title"] = self.title
        metrics_output["iou_threshold"] = self.iou_threshold
        metrics_output["single_threshold"] = fscore_metrics
        metrics_output["confidence_threshold"] = self.confidence_threshold
        if self.iou_range:
            aps, rs, ars, map, mar = self.evaluate_range(iou_range=self.iou_range)
            metrics_output["AP"] = aps
            metrics_output["rs"] = rs
            metrics_output["ars"] = ars
            metrics_output["map"] = map
            metrics_output["mar"] = mar
            metrics_output["iou_range"] = self.iou_range
        with open(os.path.join(self.output_path, self.metrics_file), "wb") as f:
            pickle.dump(metrics_output, f)
        logger.info(f"metrics saved to {os.path.join(self.output_path, self.metrics_file)}.")
        self.plot_roc_curves(fscore_metrics)
        self.plot_precision_recall_curve(fscore_metrics)
        self.generate_report(metrics_output)
        return metrics_output

    def worker(self, iou_threshold):
        basics = self.basic_metric(iou_threshold=iou_threshold, confidence_threshold=0.1)

        rs = [result["Single_Recall"] for result in basics]
        output_metrics = self.get_average_precision(basics)
        aps = [result["AP"] for result in output_metrics]
        map = sum(aps) / len(aps)
        classes = [basic["Class"] for basic in basics]
        return rs, aps, map, classes

    def evaluate_range(self, iou_range: List[float], confidence_threshold: float = None):
        # if not iou_range:
        #    iou_range = self.iou_range
        if not confidence_threshold:
            confidence_threshold = self.confidence_threshold

        aps = dict()
        rs: Dict[float, List[float]] = dict()
        map = dict()
        with Pool(self.max_workers) as pool:

            result = pool.map(self.worker, iou_range)

        for iou, res in zip(iou_range, result):
            aps[iou] = res[0]
            rs[iou] = res[1]
            map[iou] = res[2]
            classes = res[3]

        assert len(aps) == len(iou_range)
        ars = self.get_average_recall(rs, iou_range)
        self.plot_recall_iou_curve(rs, iou_range, classes)

        mar = sum(ars) / len(ars)
        return aps, rs, ars, map, mar

    def plot_recall_iou_curve(
        self, recalls: Dict[float, List[float]], iou_thresholds: List[float], classes: List[str], show_ar: bool = True
    ) -> None:
        """Plot the Recall x IOU curve for a given class.

        Args:
            recalls (Dict[float:list]): keys are iou thresholds. value is a list of recall for each class.
            iou_thresholds: list of iou thresholds.
            classes: list containing names of all classes.
        """
        # Each result represents a class
        for index, class_id in enumerate(classes):
            recall_vector = [recalls[iou][index] for iou in iou_thresholds]

            plt.close()

            plt.plot(iou_thresholds, recall_vector, label=f"Confidence:{self.confidence_threshold}")
            plt.xlabel("IOU")
            plt.ylabel("Recall")
            if show_ar:

                ap_str = "{0:.2f}%".format(sum(recall_vector) / len(recall_vector) * 100)
                plt.title("Recall x IOU curve \nClass: %s, AR: %s" % (str(class_id), ap_str))
            else:
                plt.title("Recall x IOU curve \nClass: %s" % str(class_id))
            plt.legend(shadow=True)
            plt.grid()
            plt.xlim([0.0, 1.0])
            plt.ylim([0.0, 1.0])
            plt.savefig(os.path.join(self.output_path, class_id + "_recall_iou.png"))
        plt.close()

    @property
    def templates_path(self):
        return self._templates_path

    @templates_path.setter
    def templates_path(self, path):
        os.makedirs(os.path.abspath(path), exist_ok=True)
        self._templates_path = os.path.abspath(path)

    @property
    def output_path(self):
        return self._output_path

    @output_path.setter
    def output_path(self, path):
        os.makedirs(os.path.abspath(path), exist_ok=True)
        self._output_path = os.path.abspath(path)

    @property
    def iou_threshold(self):
        return self._iou_threshold

    @iou_threshold.setter
    def iou_threshold(self, value):
        if value < 0 or value > 1:
            raise ValueError
        self._iou_threshold = value

    @property
    def confidence_threshold(self):
        return self._confidence_threshold

    @confidence_threshold.setter
    def confidence_threshold(self, value):
        if value < 0 or value > 1:
            raise ValueError
        self._confidence_threshold = value

    @uval_stage
    def data_preparations(self):

        ground_truths = []

        detections = []
        # Get all classes
        classes = []
        det_classes = []
        volumes_soc = {}
        for row_num in track(range(len(self.dataset.table)), "Preparing..."):
            row = self.dataset.table.loc[row_num]

            volume_id = row["volume_id"]
            if volume_id not in volumes_soc:
                volumes_soc[volume_id] = 0

            det = row["hdf5_detection"]
            gt = row["hdf5_groundtruth"]
            if gt:
                volumes_soc.pop(volume_id, None)
                for gt_item in gt.values():
                    class_name = gt_item["class_name"]
                    ground_truths.append(
                        DetectionEntry(volume_id, class_name, 1.0, gt_item["roi_start"], gt_item["roi_shape"])
                    )
                    if class_name not in classes:
                        classes.append(class_name)
            # Loop through all bounding boxes and separate them into GTs and
            # detections

            for det_item in det:
                # if det_item["class_name"]=="bluntobject":
                #    class_name = "bluntobjects"
                if det_item["class_name"] == "iCMORE":
                    class_name = "grenade"
                else:
                    class_name = det_item["class_name"]

                det_classes.append(class_name)
                detections.append(
                    DetectionEntry(
                        volume_id, class_name, det_item["score"], det_item["roi_start"], det_item["roi_shape"]
                    )
                )
        logger.info(f"detected classes are:{set(det_classes)}")
        logger.info(f"ground truth classes are:{set(classes)}")
        total_negative = len(volumes_soc)
        return classes, volumes_soc, ground_truths, detections, total_negative

    @uval_stage
    def basic_metric(self, iou_threshold: float = None, confidence_threshold: float = None) -> List[dict]:
        """Get the TP, FP, Precision and recall.

        Args:
            iou_threshold (float, optional): Threshold for IOU. Defaults to None.
            confidence_threshold (float, optional): Threshold for confidence. Defaults to None.

        Returns:
            List[dict]: A list of dictionaries. Each dictionary contains information and
            metrics of each class.
        """

        if not self.data:
            self.data = self.data_preparations()
        classes, volumes_soc, ground_truths, detections, total_negative = self.data
        if iou_threshold is None:
            iou_threshold = self.iou_threshold
        if confidence_threshold is None:
            confidence_threshold = self.confidence_threshold
        ret = []
        # Loop through by classes
        for c in classes:
            volumes_negative_current = {v: 0 for v in volumes_soc}

            # Get only detection of class c
            dects = [d for d in detections if d.class_name == c]
            # dects_image_level = [d.volume_id for d in detections if d.class_name == c]
            # Get only ground truths of class c, use filename as key
            gts: Dict[Any, Any] = {}
            nneg = 0.0
            npos = 0.0
            for g in ground_truths:
                if g.class_name == c:
                    # volumes that do not contain class c
                    npos += 1.0
                    gts[g.volume_id] = gts.get(g.volume_id, []) + [g]
                else:
                    nneg += 1.0

            # sort detections by decreasing confidence
            dects = sorted(dects, key=lambda detected_entry: detected_entry.confidence_score, reverse=True)
            total_tp = 0
            total_fp = 0
            fp_image_level = np.zeros(len(dects))

            tp = np.zeros(len(dects))
            fp = np.zeros(len(dects))
            tp_soft = 0
            fp_soft = 0
            # create dictionary with amount of gts for each image
            det = {key: np.zeros(len(gts[key])) for key in gts}

            # Loop through detections
            single_recall = 0.0
            for d, dect in enumerate(dects):
                if dect.confidence_score < confidence_threshold:
                    single_recall = float(np.sum(tp)) / npos
                if dect.volume_id in volumes_negative_current:
                    fp_image_level[d] = 1
                    volumes_negative_current.pop(dect.volume_id, None)

                # Find ground truth image
                gt = gts[dect.volume_id] if dect.volume_id in gts else []
                iou_max = sys.float_info.min
                for j, gtj in enumerate(gt):
                    iou = Metrics.iou(dect.roi_start, dect.roi_shape, gtj.roi_start, gtj.roi_shape)
                    if iou > iou_max:
                        iou_max = iou
                        jmax = j
                # Assign detection as true positive/don't care/false positive
                if iou_max >= iou_threshold:
                    if det[dect.volume_id][jmax] == 0:
                        tp[d] = 1  # count as true positive
                        total_tp += 1 if dect.confidence_score > confidence_threshold else 0
                        tp_soft += dect.confidence_score if dect.confidence_score > confidence_threshold else 0
                        det[dect.volume_id][jmax] = 1  # flag as already 'seen'
                    else:
                        fp[d] = 1  # count as false positive
                        total_fp += 1 if dect.confidence_score > confidence_threshold else 0
                        fp_soft += dect.confidence_score if dect.confidence_score > confidence_threshold else 0
                # - A detected "cat" is overlaped with a GT "cat" with IOU >= iou_threshold.
                else:
                    fp[d] = 1  # count as false positive
                    total_fp += 1 if dect.confidence_score > confidence_threshold else 0
                    fp_soft += dect.confidence_score if dect.confidence_score > confidence_threshold else 0
            # compute precision, recall and average precision
            acc_fp = np.cumsum(fp)
            acc_tp = np.cumsum(tp)
            acc_fp_image_level = np.cumsum(fp_image_level)
            fpr = acc_fp_image_level / total_negative
            rec = acc_tp / npos

            prec = np.divide(acc_tp, (acc_fp + acc_tp))

            # Depending on the method, call the right implementation
            # add class result in the dictionary to be returned
            r = {
                "Class": c,
                "precision": prec,
                "recall": rec,
                "Single_Recall": single_recall,
                "Total Positives": npos,
                "Total Negatives": nneg,
                "Total TP": total_tp,
                "Total FP": total_fp,
                "Total FN": npos - total_tp,
                "Total TP soft": tp_soft,
                "Total FP soft": fp_soft,
                "Total FN soft": npos - tp_soft,
                "fpr": fpr,
            }
            ret.append(r)

        return ret

    def get_pascal_voc2012_metric(self, confidence_threshold=None) -> list:
        basics = self.basic_metric(iou_threshold=0.5, confidence_threshold=confidence_threshold)
        return self.get_average_precision(basics, method="EveryPointInterpolation")

    def get_pascal_voc2007_metric(self, confidence_threshold=None) -> list:
        basics = self.basic_metric(iou_threshold=0.5, confidence_threshold=confidence_threshold)
        return self.get_average_precision(basics, method="ElevenPointInterpolation")

    @uval_stage
    def get_average_recall(self, recalls: Dict[float, list], iou_range: List) -> List:
        class_num = len(recalls[iou_range[0]])
        average_recalls = [0] * class_num
        for c in range(class_num):
            area = 0
            for idx in range(len(iou_range) - 1):
                iou_step = iou_range[idx + 1] - iou_range[idx]
                area += iou_step * (
                    recalls[iou_range[idx]][c] + 0.5 * (recalls[iou_range[idx]][c] - recalls[iou_range[idx + 1]][c])
                )
            average_recalls[c] = area
        return average_recalls

    @uval_stage
    def get_average_precision(self, basic_metrics: List[dict], method: str = None) -> List[dict]:
        """Get the average precision. This will be used in multiple other metrics such as
        COCO or pascal voc.

        Args:
            basic_metrics (List[dict]): [description]
            method (str, optional): choice between precise (EveryPointInterpolation or None)
            or estimation (ElevenPointInterpolation). Defaults to None.

        Returns:
            List[dict]: adds ap to the each class of the output dictionaries.
        """

        if method is None:
            method = self.ap_method
        ret = []
        for err in basic_metrics:
            # Depending on the method, call the right implementation
            if method == "EveryPointInterpolation":
                [ap, mpre, mrec] = Metrics.calculate_average_precision(err["recall"], err["precision"])
            else:
                [ap, mpre, mrec] = Metrics.eleven_point_interpolated_ap(err["recall"], err["precision"])
            # add class result in the dictionary to be returned
            r = {key: value for key, value in err.items()}
            r["AP"] = ap
            r["interpolated precision"] = mpre
            r["interpolated recall"] = mrec

            ret.append(r)
        return ret

    @uval_stage
    def get_fscore(self, basic_metrics: List[dict]) -> List[dict]:
        """Get the f score metrics.

        Args:
            basic_metrics (List[dict]): output of basic_metric method.
            needs to be called before this method.

        Returns:
            List[dict]: adds dict['F score'] and dict['F score soft'] to the inputs.
        """

        ret = []
        for err in basic_metrics:
            fp = err["Total FP"]
            fn = err["Total FN"]
            tp = err["Total TP"]
            f_score = (1 + self.factor**2) * tp / ((1 + self.factor**2) * tp + (self.factor**2) * fn + fp)

            fp_soft = err["Total FP soft"]
            fn_soft = err["Total FN soft"]
            tp_soft = err["Total TP soft"]
            f_score_soft = (
                (1 + self.factor**2)
                * tp_soft
                / ((1 + self.factor**2) * tp_soft + (self.factor**2) * fn_soft + fp_soft)
            )
            # add class result in the dictionary to be returned
            r = {key: value for key, value in err.items()}
            r["F score"] = f_score
            r["F score soft"] = f_score_soft
            ret.append(r)
        return ret

    @uval_stage
    def generate_report(self, results_cluttered: dict) -> None:
        # Sample DataFrame
        range_results = dict(results_cluttered)
        single_results = range_results.pop("single_threshold")

        def func(row):

            highlight = "background-color: darkorange;"
            default = ""

            return [default] * (len(row) - 1) + [highlight]

        classes = []
        for idx, res in enumerate(single_results):
            res.pop("precision")
            res.pop("recall")
            res.pop("fpr")
            res.pop("interpolated precision")
            res.pop("interpolated recall")
            # res["ar"]=range_results["ars"][idx]
            classes.append(res["Class"])
            res.pop("Class")
        # for key, value in kwargs.items():
        high_level = dict()
        range_results.pop("ap", None)
        rs = range_results.pop("rs", None)
        range_results.pop("ars", None)
        range_results.pop("iou_range", None)
        high_level["mar"] = range_results.pop("mar", None)

        cell_hover = {  # for row hover use <tr> instead of <td>
            "selector": "td:hover",
            "props": [("background-color", "#ffffb3")],
        }
        row_hover = {  # for row hover use <tr> instead of <td>
            "selector": "tr:hover",
            "props": [("background-color", "#ffffb3")],
        }
        sorted_idx = [i[0] for i in sorted(enumerate(classes), key=lambda x: x[1])]
        single_results_sorted = [single_results[i] for i in sorted_idx]
        df = pd.DataFrame(single_results_sorted, index=pd.Index(sorted(classes)))

        styler = (
            df.style.set_caption(f"Calculated metrics for iou:{self.iou_threshold}")
            # .set_precision(2)
            .format(precision=2).set_table_styles([row_hover])
        )
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=self.templates_path))
        template = env.get_template(self.template_file)
        total_images = []

        for cls in sorted(classes):
            img_names = []
            img_names.append("." + "/" + cls + "_roc.png")
            img_names.append("." + "/" + cls + "_precision_recall.png")
            if self.iou_range:
                img_names.append("." + "/" + cls + "_recall_iou.png")
            total_images.append(img_names)

        if self.iou_range:
            high_level["map"] = sum(range_results["map"].values()) / len(range_results["map"])
            range_results["map"]["Total"] = high_level["map"]
            df2 = pd.DataFrame(
                [range_results["map"].values()], index=pd.Index(["map"]), columns=range_results["map"].keys()
            )
            rs_sorted = {key: [val[i] for i in sorted_idx] for key, val in rs.items()}
            df_rs = pd.DataFrame(rs_sorted, index=pd.Index(sorted(classes)))
            styler_rs = (
                df_rs.style.set_caption("Recall values for all classes and all IOU thresholds")
                .format(precision=2)
                .set_table_styles([row_hover])
            )

            styler2 = (
                df2.style.set_caption("Mean average precision for various IOU levels.")
                .format(precision=2)
                .set_table_styles([cell_hover])
                .apply(func, subset=["Total"], axis=1)
            )

            # Template handling

            html = template.render(
                range_table=styler2.to_html(),
                single_table=styler.to_html(),
                rs_table=styler_rs.to_html(),
                total_images=total_images,
                mar=round(high_level["mar"], 2),
                map=round(high_level["map"], 2),
                title=self.title,
            )
        else:
            html = template.render(single_table=styler.to_html(), total_images=total_images, title=self.title)
            # Template handling

        # Write the HTML file
        with open(os.path.join(self.output_path, self.report_file), "w") as f:
            f.write(html)
        logger.info(f"Report saved to {os.path.join(self.output_path, self.report_file)}.")

    @uval_stage
    def plot_precision_recall_curve(
        self,
        pascal_voc_metrics: List[dict],
        show_ap: bool = True,
        show_interpolated_precision: bool = True,
        show_graphic: bool = False,
    ) -> None:
        """Plot the Precision x Recall curve for a given class.

        Args:
            pascal_voc_metrics (List[dict]): Output of some pascal voc metric. needs to be
            called before this method.
            show_ap (bool, optional): if True, the average precision value will be shown
            in the title of the graph. Defaults to False.
            show_interpolated_precision (bool, optional): if True, it will show in the plot
            the interpolated precision. Defaults to False.
            show_graphic (bool, optional): if True, the plot will be shown. Defaults to False.

        Raises:
            IOError: [description]
        """

        result = None
        # Each result represents a class
        for result in pascal_voc_metrics:
            if result is None:
                raise IOError("Error: No data for a class was found.")

            class_id = result["Class"]
            precision = result["precision"]
            recall = result["recall"]
            average_precision = result["AP"]
            mpre = result["interpolated precision"]
            mrec = result["interpolated recall"]

            plt.close()
            if show_interpolated_precision:
                if self.ap_method == "EveryPointInterpolation":
                    plt.plot(mrec, mpre, "--r", label="Interpolated precision (every point)")
                elif self.ap_method == "ElevenPointInterpolation":
                    # Uncomment the line below if you want to plot the area
                    # plt.plot(mrec, mpre, 'or', label='11-point interpolated precision')
                    # Remove duplicates, getting only the highest precision of
                    # each recall value
                    nrec = []
                    nprec = []
                    for idx in range(len(mrec)):
                        r = mrec[idx]
                        if r not in nrec:
                            idx_eq = np.argwhere(mrec == r)
                            nrec.append(r)
                            nprec.append(max([mpre[int(idx)] for idx in idx_eq]))
                    plt.plot(nrec, nprec, "or", label="11-point interpolated precision")
                else:
                    raise NotImplementedError(
                        "plot_precision_recall_curve() without show_interpolated_precision is not implemented yet!"
                    )
            plt.plot(recall, precision, label=f"Precision for IOU:{self.iou_threshold}")
            plt.xlabel("recall")
            plt.ylabel("precision")
            if show_ap:
                ap_str = "{0:.2f}%".format(average_precision * 100)
                plt.title("Precision x Recall curve \nClass: %s, AP: %s" % (str(class_id), ap_str))
            else:
                plt.title("Precision x Recall curve \nClass: %s" % str(class_id))
            plt.legend(shadow=True)
            plt.grid()

            plt.xlim([0.0, 1.0])
            plt.ylim([0.0, 1.0])
            if self.output_path is not None:
                plt.savefig(os.path.join(self.output_path, class_id + "_precision_recall.png"))

            if show_graphic is True:
                plt.show(block=False)
                plt.pause(0.05)
        plt.close()

    @staticmethod
    def calculate_average_precision(rec: List[float], prec: List[float]) -> List[Any]:
        assert len(rec) == len(prec)
        mrec = [0.0] + list(rec) + [1.0]
        mpre = [1.0] + list(prec) + [0.0]
        for i in range(len(mpre) - 1, 0, -1):
            mpre[i - 1] = max(mpre[i - 1], mpre[i])
        ii = []
        for i in range(len(mrec) - 1):
            if mrec[1 + i] != mrec[i]:
                ii.append(i + 1)
        ap: Union[float, Any] = 0.0
        for i in ii:
            ap = ap + np.sum((mrec[i] - mrec[i - 1]) * mpre[i])
        # return [ap, mpre[1:len(mpre)-1], mrec[1:len(mpre)-1], ii]
        return [ap, mpre[0 : len(mpre) - 1], mrec[0 : len(mpre) - 1]]

    @staticmethod
    # 11-point interpolated average precision
    def eleven_point_interpolated_ap(rec: List[float], prec: List[float]) -> List[Any]:
        mrec = list(rec)
        mpre = list(prec)
        recall_values_np = np.linspace(0, 1, 11)
        recall_values = list(recall_values_np[::-1])
        rho_interp = []
        recall_valid = []
        # For each recall_values (0, 0.1, 0.2, ... , 1)
        for r in recall_values:
            # Obtain all recall values higher or equal than r
            arg_greater_recalls = np.argwhere(mrec[:] >= r)
            pmax = 0.0
            # If there are recalls above r
            if arg_greater_recalls.size != 0:
                pmax = max(mpre[int(arg_greater_recalls.min()) :])
            recall_valid.append(r)
            rho_interp.append(pmax)
        # By definition ap = sum(max(precision whose recall is above r))/11
        ap = sum(rho_interp) / 11
        # Generating values for the plot
        rvals = [recall_valid[0]] + list(recall_valid) + [0.0]
        pvals = [0.0] + list(rho_interp) + [0.0]
        # rho_interp = rho_interp[::-1]
        cc = []
        for i in range(len(rvals)):
            p = (rvals[i], pvals[i - 1])
            if p not in cc:
                cc.append(p)
            p = (rvals[i], pvals[i])
            if p not in cc:
                cc.append(p)
        recall_values_out = [i[0] for i in cc]
        rho_interp = [i[1] for i in cc]
        return [ap, rho_interp, recall_values_out]

    @staticmethod
    def iou(start_a: List[float], shape_a: List[float], start_b: List[float], shape_b: List[float]) -> float:
        """Calculates the intersection over union of the two cubes A and B.

        Args:
            start_a (List[float]): bottom left corner of the cube A.
            shape_a (List[float]): size of each dimension in the cube A.
            start_b (List[float]): bottom left corner of the cube B.
            shape_b (List[float]): size of each dimension in the cube B.

        Returns:
            float: 3D IOU of these cubes.
        """

        if (
            np.any(np.array(start_a) < 0)
            or np.any(np.array(start_b) < 0)
            or np.any(np.array(shape_a) < 0)
            or np.any(np.array(shape_b) < 0)
        ):
            logger.warning(f"bounding box coordinates are negative!{start_a}{shape_a}{start_b}{shape_b}")
            return 0

        if Metrics._boxes_intersect(start_a, shape_a, start_b, shape_b) is False:
            return 0
        inter_area = Metrics._get_intersection_area(start_a, shape_a, start_b, shape_b)
        union = Metrics._get_union_areas(start_a, shape_a, start_b, shape_b)
        # intersection over union
        iou = inter_area / union
        assert iou >= 0
        return iou

    @staticmethod
    def _boxes_intersect(
        start_a: List[float], shape_a: List[float], start_b: List[float], shape_b: List[float]
    ) -> bool:
        """Check if the two cubes intersect or not.

        Args:
            start_a (List[float]): bottom left corner of the cube A.
            shape_a (List[float]): size of each dimension in the cube A.
            start_b (List[float]): bottom left corner of the cube B.
            shape_b (List[float]): size of each dimension in the cube B.

        Returns:
            bool: True if the two cubes intersect. otherwise False.
        """

        if start_a[0] > start_b[0] + shape_b[0]:
            return False
        if start_b[0] > start_a[0] + shape_a[0]:
            return False
        if start_a[1] > start_b[1] + shape_b[1]:
            return False
        if start_b[1] > start_a[1] + shape_a[1]:
            return False
        if start_a[2] > start_b[2] + shape_b[2]:
            return False
        if start_b[2] > start_a[2] + shape_a[2]:
            return False
        return True

    @staticmethod
    def _get_union_areas(
        start_a: List[float], shape_a: List[float], start_b: List[float], shape_b: List[float]
    ) -> float:
        """Calculates the Union of the areas of the two cubes A and B.

        Args:
            start_a (List[float]): bottom left corner of the cube A.
            shape_a (List[float]): size of each dimension in the cube A.
            start_b (List[float]): bottom left corner of the cube B.
            shape_b (List[float]): size of each dimension in the cube B.

        Returns:
            float: union of the two cubes.
        """
        area_a = Metrics._get_area(shape_a)
        area_b = Metrics._get_area(shape_b)
        inter_area = Metrics._get_intersection_area(start_a, shape_a, start_b, shape_b)
        return float(area_a + area_b - inter_area)

    @staticmethod
    def _get_area(shape: List[float]) -> float:
        """calculates the area of a cube.

        Args:
            shape (List[float]): size of each dimension in the cube.

        Returns:
            float: area of the cube.
        """

        return math.prod(shape)

    @staticmethod
    def _get_intersection_area(
        start_a: List[float], shape_a: List[float], start_b: List[float], shape_b: List[float]
    ) -> float:
        """Calculates the intersection of the areas of the two cubes A and B.

        Args:
            start_a (List[float]): bottom left corner of the cube A.
            shape_a (List[float]): size of each dimension in the cube A.
            start_b (List[float]): bottom left corner of the cube B.
            shape_b (List[float]): size of each dimension in the cube B.

        Returns:
            float: intersection of the two cubes.
        """
        x_a = max(start_a[0], start_b[0])
        y_a = max(start_a[1], start_b[1])
        z_a = max(start_a[2], start_b[2])
        x_b = min(start_a[0] + shape_a[0], start_b[0] + shape_b[0])
        y_b = min(start_a[1] + shape_a[1], start_b[1] + shape_b[1])
        z_b = min(start_a[2] + shape_a[2], start_b[2] + shape_b[2])
        # intersection area
        return (x_b - x_a) * (y_b - y_a) * (z_b - z_a)

    @uval_stage
    def plot_roc_curves(self, roc_metrics: List[dict], show_graphic: bool = False) -> None:
        """Plot the ROC curve for every class.

        Args:
            roc_metrics (List[dict]): Output of some basic_metric. needs to be
            called before this method.
            show_graphic (bool, optional): if True, the plot will be shown. Defaults to False.

        Raises:
            IOError: [description]
        """

        result = None
        # Each resut represents a class
        for result in roc_metrics:
            if result is None:
                raise IOError("Error:No data for this class could be found.")

            class_id = result["Class"]

            recall = result["recall"]
            fpr = result["fpr"]

            plt.close()
            plt.plot(fpr, recall, label=f"ROC for IOU:{self.iou_threshold}")
            plt.xlabel("FP Rate")
            plt.ylabel("TP Rate")
            plt.title("ROC curve \nClass: %s" % str(class_id))
            plt.legend(shadow=True)
            plt.grid()
            plt.xlim([0.0, 1.0])
            plt.ylim([0.0, 1.0])
            if self.output_path is not None:
                plt.savefig(os.path.join(self.output_path, class_id + "_roc.png"))
            if show_graphic is True:
                plt.show(block=False)
                plt.pause(0.05)
        plt.close()
