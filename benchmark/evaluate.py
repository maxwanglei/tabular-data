from typing import Any
import pandas as pd
from pandas import DataFrame, Series
import math
import functools
import logging

from extractor.utils import (
    extract_float_value,
    extract_float_values,
)

logger = logging.getLogger(__name__)

"""
row count:      10/100
Parameter type: 10/100
Value:          20/100 
Unit:           10/100  
Time:           10/100 
Time unit:      10/100 
Subjects:       15/100 
Drug Name:      15/100 
"""

DELTA_VALUE = 0.000001
SIMILARITY_DISTANCE_THRESHOLD = 0.5


def is_abbreviation_or_contraction(a: str, b: str):
    if a is None or b is None:
        return False
    a = a.strip()
    b = b.strip()
    if len(a) == 0 and len(b) == 0:
        return True
    if len(a) == 0 or len(b) == 0:
        return False
    short = a.lower() if len(a) < len(b) else b.lower()
    long = a.lower() if len(a) >= len(b) else b.lower()
    start_ix = 0
    matches = False
    for c in short:
        if not ((c >= "a" and c <= "z") or (c >= "A" and c <= "Z")):
            continue
        ix = long.find(c, start_ix)
        if ix < start_ix:
            return False
        matches = True
        start_ix = ix + 1
    return matches


def is_values_in_strings_equaled(a: str, b: str):
    if a is None and b is None:
        return True
    if a is None or b is None:
        return False
    vals1 = extract_float_values(a)
    vals2 = extract_float_values(b)
    if vals1 is None and vals2 is None:
        return True
    if vals1 is None or vals2 is None:
        return False
    if len(vals1) != len(vals2):
        return False
    for ix in range(len(vals1)):
        if vals1[ix] != vals2[ix]:
            return False
    return True


class TextComparer:
    def __init__(self) -> None:
        from sentence_transformers import SentenceTransformer

        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    def compare(self, a, b) -> float:
        if is_abbreviation_or_contraction(a, b):
            return 1.0
        if not is_values_in_strings_equaled(a, b):
            return 0.0

        from sentence_transformers import util

        embedding_1 = self.model.encode(a, convert_to_tensor=True)
        embedding_2 = self.model.encode(b, convert_to_tensor=True)
        dist = util.pytorch_cos_sim(embedding_1, embedding_2)
        return dist[0][0].item()


class TablesEvaluator:
    def __init__(self, rating_cols: list[str], anchor_cols: list[str]):
        self.rating_cols = rating_cols
        self.anchor_cols = anchor_cols
        self.text_cmpr = TextComparer()

    def anchor_row(self, row1: Series, row2: Series):
        # locate row by anchor columns
        for c in self.anchor_cols:
            v1 = row1[c]
            v2 = row2[c]
            if not self.is_equal(v1, v2):
                return False
        return True

    def rate_row(self, row1: Series, row2: Series) -> int:
        sum = 0
        for c in self.rating_cols:
            v1 = row1[c]
            v2 = row2[c]

            if self.is_equal(v1, v2):
                sum += 1

        return (int)(10.0 * sum / float(len(self.rating_cols)))

    @staticmethod
    def parse_value(val: Any) -> int | float | None:
        if isinstance(val, (int, float)) and not math.isnan(val):
            return val
        if not isinstance(val, str):
            return None
        try:
            return int(val)
        except ValueError:
            pass
        try:
            return float(val)
        except ValueError:
            return None

    def is_equal(self, v1, v2) -> bool:
        if v1 == v2:
            return True
        if isinstance(v1, str) and isinstance(v2, str):
            dist = self.text_cmpr.compare(v1, v2)
            # output_msg(f"{dist} = [{v1}] - [{v2}]")
            return (
                dist >= SIMILARITY_DISTANCE_THRESHOLD
            )  # v1.strip().lower() == v2.strip().lower()
        if not isinstance(v1, str) and not isinstance(v2, str):
            if math.isnan(v1) and math.isnan(v2):
                return True
            fv1 = float(v1)
            fv2 = float(v2)
            return abs(fv1 - fv2) < DELTA_VALUE

        # One of the two values is str
        sval = v1.strip() if isinstance(v1, str) else v2.strip()
        nsval = v1 if not isinstance(v1, str) else v2
        if math.isnan(nsval):
            sval = sval.strip()
            if len(sval) == 0:
                return True
            try:
                tmp = float(sval)
            except ValueError:
                return True
        try:
            fv1 = extract_float_value(sval) if len(sval) > 0 else math.nan
            fv2 = float(nsval)
            if fv1 is None:
                return False if not math.isnan(fv2) else True
            return abs(fv1 - fv2) < DELTA_VALUE
        except Exception as e:
            logger.error(e)
            return False

    def anchor_row_from_rows(self, row: Series, rows: list[Series]):
        candidate_rows = rows
        similar_rows = []
        for c in self.anchor_cols:
            v = row[c]
            if v is None:
                continue
            v = v.strip() if isinstance(v, str) else v
            if isinstance(v, str) and len(v) == 0:
                continue
            similar_rows = []
            for r in candidate_rows:
                if self.is_equal(v, r[c]):
                    similar_rows.append(r)
            if len(similar_rows) == 0:
                candidate_rows = rows
            elif len(similar_rows) == 1:
                return similar_rows[0]
            else:
                candidate_rows = similar_rows
        return None if len(similar_rows) == 0 else similar_rows[0]

    def rate_rows(self, baseline: DataFrame, target: DataFrame) -> int:
        bshape = baseline.shape
        tshape = target.shape
        if bshape[1] != tshape[1]:
            return 0

        less = baseline if bshape[0] <= tshape[0] else target
        much = baseline if bshape[0] > tshape[0] else target
        less_row_num = less.shape[0]
        much_row_num = much.shape[0]
        scores = []
        sum = 0
        much_rows = much.to_dict("records")
        for index, row in less.iterrows():
            much_row = self.anchor_row_from_rows(row, much_rows)
            if much_row is None:
                scores.append(0)
                continue
            scores.append(self.rate_row(row, much_row))

        sum = functools.reduce(lambda a, b: a + b, scores)
        logger.info(f"scores: {scores}")
        logger.info(f"less row number: {less_row_num}, much row number: {much_row_num}")
        return (int)(
            100.0 * (sum / (10.0 * less_row_num + 1 * (much_row_num - less_row_num)))
        )

    def compare_tables(self, baseline: pd.DataFrame, target: pd.DataFrame) -> int:
        return self.rate_rows(baseline, target)
