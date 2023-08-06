# ONLY testing one function from feature_engineering. Would be good to expand this
# if we have some spare time in a sprint
import numpy as np
import pandas as pd
import pytest
from cognite.client import CogniteClient
from pandas.testing import assert_frame_equal

from akerbp.mlpet import feature_engineering
from akerbp.mlpet.tests.data.data import (
    FORMATION_DF,
    FORMATION_TOPS_MAPPER,
    TEST_DF,
    VERTICAL_DEPTHS_MAPPER,
    VERTICAL_DF,
)

client = CogniteClient(client_name="test", project="akbp-subsurface")


def test_add_formations_and_groups_using_mapper():
    df_with_tops = feature_engineering.add_formations_and_groups(
        FORMATION_DF[["DEPTH", "well_name"]],
        formation_tops_mapper=FORMATION_TOPS_MAPPER,
        id_column="well_name",
    )
    # Sorting columns because column order is not so important
    assert_frame_equal(df_with_tops.sort_index(axis=1), FORMATION_DF.sort_index(axis=1))


def test_add_formations_and_groups_using_client():
    df_with_tops = feature_engineering.add_formations_and_groups(
        FORMATION_DF[["DEPTH", "well_name"]],
        id_column="well_name",
        client=client,
    )
    assert_frame_equal(df_with_tops.sort_index(axis=1), FORMATION_DF.sort_index(axis=1))


def test_add_formations_and_groups_raises_exception_if_no_client_nor_mapping_is_provided():
    with pytest.raises(
        Exception,
        match="Neither a formation tops mapping nor cognite client is provided. Not able to add formation tops to dataset",
    ):
        _ = feature_engineering.add_formations_and_groups(
            FORMATION_DF[["DEPTH", "well_name"]],
            id_column="well_name",
        )


def test_add_vertical_depths_using_mapper():
    df_with_vertical_depths = feature_engineering.add_vertical_depths(
        VERTICAL_DF[["DEPTH", "well_name"]],
        vertical_depths_mapper=VERTICAL_DEPTHS_MAPPER,
        id_column="well_name",
        md_column="DEPTH",
    )

    assert_frame_equal(
        df_with_vertical_depths.sort_index(axis=1), VERTICAL_DF.sort_index(axis=1)
    )


def test_add_vertical_depths_using_client():
    df_with_vertical_depths = feature_engineering.add_vertical_depths(
        VERTICAL_DF[["DEPTH", "well_name"]],
        id_column="well_name",
        md_column="DEPTH",
        client=client,
    )

    assert_frame_equal(
        df_with_vertical_depths.sort_index(axis=1), VERTICAL_DF.sort_index(axis=1)
    )


def test_add_vertical_depths_raises_expection_if_no_client_nor_mapping_is_provided():
    with pytest.raises(
        Exception,
        match="Neither a vertical depths mapping nor a cognite client is provided. Not able to add vertical depths to dataset",
    ):
        _ = feature_engineering.add_vertical_depths(
            VERTICAL_DF[["DEPTH", "well_name"]],
            id_column="well_name",
            md_column="DEPTH",
        )


def test_add_well_metadata():
    metadata = {"30/11-6 S": {"FOO": 0}, "25/7-4 S": {"FOO": 1}}
    df = feature_engineering.add_well_metadata(
        TEST_DF, metadata_dict=metadata, metadata_columns=["FOO"], id_column="well_name"
    )
    assert "FOO" in df.columns.tolist()


def test_guess_bs_from_cali():
    input = pd.DataFrame({"CALI": [6.1, 5.9, 12.0, 12.02]})
    df = feature_engineering.guess_BS_from_CALI(input)
    assert "BS" in df.columns.tolist()


def test_calculate_cali_bs():
    input = pd.DataFrame({"CALI": np.array([6.1, 5.9, 12.0, 12.02])})
    df = feature_engineering.calculate_CALI_BS(input)
    assert "CALI-BS" in df.columns.tolist()


def test_calculate_VSH():
    df = client.sequences.data.retrieve_dataframe(
        id=3562899615737883, start=None, end=None
    )
    df["well"] = "dummy"
    df_out = feature_engineering.calculate_VSH(
        df,
        groups_column_name="GROUP",
        formations_column_name="FORMATION",
        id_column="well",
    )
    assert "VSH" in df_out.columns.tolist()
    assert not df_out["VSH"].isnull().values.any()
