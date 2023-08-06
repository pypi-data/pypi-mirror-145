import os
from typing import Dict, List, cast

import jinja2
import pandas as pd  # type: ignore
from matplotlib import pyplot as plt  # type: ignore

from uval.stages.stage import uval_stage  # type: ignore
from uval.utils.log import logger


class DiffReporter:
    """This class implements a comparison for atleast two methods.
    The basic UVal analysis should have been performed beforehand.
    """

    def __init__(self, models: List[Dict]) -> None:

        self.models = models
        if all(["iou_range" in model.keys() for model in models]):
            self.report_type = "RANGE"
        else:
            self.report_type = "SINGLE"
        name = "_".join([str(result.get("title")) for result in models])

        self.output_path = os.path.join(".", name)
        os.makedirs(os.path.join(".", name), exist_ok=True)
        threshold = {model.get("iou_threshold") for model in models}
        assert len(threshold) == 1
        self.iou_threshold = threshold.pop()
        self.classes = sorted([result["Class"] for result in models[0]["single_threshold"]])
        self.template_file = "template_range_diff.html" if self.report_type == "RANGE" else "template_diff.html"
        self.templates_path = "src/uval/templates"
        self.report_file = "report_diff.html"

    def run(self):
        """This function performs the comparison. plots and generates the report."""
        self.plot_roc_curves(self.models)
        self.plot_precision_recall_curve(self.models)
        if self.report_type == "RANGE":
            self.plot_recall_iou_curve(self.models)
        self.generate_report(self.models)

    @uval_stage
    def plot_roc_curves(self, models: List[Dict]) -> None:
        """Plot the ROC curve for every class.

        Args:
            models (List[dict]): Output of Uval analysis for at least two methods.
        """

        result = None
        models_single: List[list] = [cast(list, model.get("single_threshold")) for model in models]
        classes = {result["Class"] for model in models_single for result in model}
        n_cls = {len(model) for model in models_single}
        # All models should have the same classes in the results
        assert len(n_cls) == 1
        n_classes = n_cls.pop()
        assert len(classes) == n_classes
        # Each result represents a class
        for class_id in classes:
            plt.close()
            for model_single, model in zip(models_single, models):
                contestant = model.get("title")
                result = next(filter(lambda x: x["Class"] == class_id, model_single))
                recall = result["recall"]
                fpr = result["fpr"]
                plt.plot(fpr, recall, label=f"ROC for IOU:{self.iou_threshold}, model:{contestant}")

            plt.xlabel("FP Rate")
            plt.ylabel("TP Rate")
            plt.title("ROC curve \nClass: %s" % str(class_id))
            plt.legend(shadow=True)
            plt.grid()
            plt.xlim([0.0, 1.0])
            plt.ylim([0.0, 1.0])
            if self.output_path is not None:
                plt.savefig(os.path.join(self.output_path, class_id + "_roc.png"))
            plt.close()

    @uval_stage
    def plot_precision_recall_curve(self, pascal_voc_metrics: List[Dict]) -> None:
        """Plot the Precision x Recall curve for a given class.

        Args:
            models (List[dict]): Output of Uval analysis for at least two methods.
        """

        def value_picker(x, idx, field):
            return x[idx].get(field)

        # Each result represents a class
        for cls in self.classes:
            plt.close()
            for model in pascal_voc_metrics:
                contestant = model["title"]
                idx = [c["Class"] for c in model["single_threshold"]].index(cls)
                precision = value_picker(model["single_threshold"], idx, "precision")
                recall = value_picker(model["single_threshold"], idx, "recall")
                average_precision = value_picker(model["single_threshold"], idx, "AP")
                plt.plot(
                    recall,
                    precision,
                    label=(
                        f"Precision for IOU:{self.iou_threshold},"
                        + f"Model:{contestant},"
                        + f"AP={(average_precision):{5}.{3}}"
                    ),
                )

            plt.xlabel("recall")
            plt.ylabel("precision")

            plt.title("Precision x Recall curve \nClass:" + cls)
            plt.legend(shadow=True)
            plt.grid()

            plt.xlim([0.0, 1.0])
            plt.ylim([0.0, 1.0])
            plt.savefig(os.path.join(self.output_path, cls + "_precision_recall.png"))

            plt.close()

    @uval_stage
    def plot_recall_iou_curve(self, models: List[Dict]) -> None:
        """Plot the Recall x IOU curve for a given class.

        Args:
            models (List[dict]): Output of Uval analysis for at least two methods.
        """
        # Each result represents a class
        for cls in self.classes:

            plt.close()
            for model in models:
                contestant = model["title"]
                idx = [c["Class"] for c in model["single_threshold"]].index(cls)

                iou_thresholds = model["iou_range"]
                recall_vector = [model.get("rs").get(iou)[idx] for iou in iou_thresholds]  # type:ignore
                ap_str = "{0:.2f}%".format(sum(recall_vector) / len(recall_vector) * 100)

                plt.plot(
                    iou_thresholds,
                    recall_vector,
                    label=f"Confidence:{model.get('confidence_threshold')}, Model: {contestant}, AP: {ap_str}",
                )
            plt.xlabel("IOU")
            plt.ylabel("Recall")

            plt.title(f"Recall x IOU curve \nClass: {cls}")

            plt.legend(shadow=True)
            plt.grid()
            plt.xlim([0.0, 1.0])
            plt.ylim([0.0, 1.0])
            plt.savefig(os.path.join(self.output_path, cls + "_recall_iou.png"))
            plt.close()

    @uval_stage
    def generate_report(self, models: List[Dict]) -> None:
        """_summary_

        Args:
            models (List[Dict]): Result of UVal analysis on atleast two methods.
        """
        # Sample DataFrame
        range_results = [dict(model) for model in models]
        single_results = [result.pop("single_threshold") for result in range_results]
        contestants = [str(result.get("title")) for result in range_results]

        def func(row):

            highlight = "background-color: darkorange;"
            default = ""

            return [default] * (len(row) - 1) + [highlight]

        classes = self.classes
        to_remove = ["precision", "recall", "fpr", "interpolated precision", "interpolated recall"]
        [r.pop(field) for field in to_remove for res in single_results for r in res]
        # [r.pop("Class") for r in res]
        # for key, value in kwargs.items():
        high_level = dict()
        to_remove = ["ap", "ars", "iou_range"]
        [r.pop(field, None) for field in to_remove for r in range_results]
        rs = [r.pop("rs", None) for r in range_results]
        high_level["mar"] = [r.pop("mar", None) for r in range_results]

        cell_hover = {  # for row hover use <tr> instead of <td>
            "selector": "td:hover",
            "props": [("background-color", "#ffffb3")],
        }
        row_hover = {  # for row hover use <tr> instead of <td>
            "selector": "tr:hover",
            "props": [("background-color", "#ffffb3")],
        }

        sorted_idx = []
        single_results_sorted = []
        for model in single_results:
            m_cls = [m.get("Class") for m in model]
            s_idx = [i[0] for i in sorted(enumerate(m_cls), key=lambda x: x[1])]
            single_results_sorted.append([model[i] for i in s_idx])
            sorted_idx.append(s_idx)

        pd_index = [val for val in contestants for _ in range(len(classes))]
        columns = list(single_results_sorted[0][0].keys())

        df = pd.DataFrame(
            [r.values() for result in single_results_sorted for r in result], index=pd.Index(pd_index), columns=columns
        )

        styler = (
            df.style.set_caption(f"Calculated metrics for iou:{self.iou_threshold}")
            # .set_precision(2)
            .format(precision=2).set_table_styles([row_hover])
        )
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=self.templates_path))
        template = env.get_template(self.template_file)
        total_images = []

        for cls in classes:
            img_names = []
            img_names.append("." + "/" + cls + "_roc.png")
            img_names.append("." + "/" + cls + "_precision_recall.png")
            if self.report_type == "RANGE":
                img_names.append("." + "/" + cls + "_recall_iou.png")
            total_images.append(img_names)

        # TODO if exists
        if self.report_type == "RANGE":
            for result in range_results:
                result["map"]["Total"] = sum(result["map"].values()) / len(result["map"])
            columns = list(range_results[0]["map"].keys())
            df2 = pd.DataFrame(
                [result["map"].values() for result in range_results],
                index=pd.Index(contestants),
                columns=[str(round(c, 2)) if isinstance(c, float) else c for c in columns],
            )
            rs_sorted = []
            for k in range(len(sorted_idx)):
                rs_sorted.append({key: [val[i] for i in sorted_idx[k]] for key, val in rs[k].items()})

            pd_index = [val for val in contestants for _ in range(len(classes))]
            pd_lines = []
            for c in range(len(classes)):
                for result in rs_sorted:
                    pd_lines.append([classes[c]] + [v[c] for v in result.values()])
            df_rs = pd.DataFrame(
                pd_lines, index=pd.Index(pd_index), columns=["Class"] + [str(e) for e in list(rs_sorted[0].keys())]
            )

            styler_rs = (
                df_rs.style.set_caption("Recall values for all classes and all IOU thresholds")
                .format(precision=2)
                .set_table_styles([row_hover])
            )

            styler2 = (
                df2.style.set_caption("Mean average precision for various IOU levels.")
                .format(precision=2)
                .set_table_styles([cell_hover])
                # .apply(func, subset=["Total"], axis=1)
            )

            # Template handling

            html = template.render(
                range_table=styler2.to_html(),
                single_table=styler.to_html(),
                rs_table=styler_rs.to_html(),
                total_images=total_images,
                # mar=round(high_level["mar"][0], 2),
                mar=" vs. ".join(
                    [contestants[r] + ":" + str(round(high_level["mar"][r], 2)) for r in range(len(range_results))]
                ),
                map=" vs. ".join(
                    [
                        contestants[r] + ":" + str(round(range_results[r]["map"]["Total"], 2))
                        for r in range(len(range_results))
                    ]
                ),
                # map=round(high_level["map"][0], 2),
                title=" x ".join(contestants),
            )
        else:
            html = template.render(
                single_table=styler.to_html(), total_images=total_images, title=" x ".join(contestants)
            )
            # Template handling

        # Write the HTML file
        with open(os.path.join(self.output_path, self.report_file), "w") as f:
            f.write(html)
        logger.info(f"Report saved to {os.path.join(self.output_path, self.report_file)}.")
