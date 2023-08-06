import warnings
from collections import defaultdict
from typing import Any, Dict, List, Union

import numpy as np
import pandas as pd
from cognite.client import CogniteClient
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter

from akerbp.mlpet import utilities


def add_log_features(
    df: pd.DataFrame,
    **kwargs,
) -> pd.DataFrame:
    """
    Creates columns with log10 of curves. All created columns are suffixed with
    '_log'. All negative values are set to zero and 1 is added to all values. In
    other words, this function is synonymous of numpy's log1p.

    Args:
        df (pd.DataFrame): dataframe with columns to calculate log10 from

    Keyword Args:
        log_features (list, optional): list of column names for the columns that should be
            loggified. Defaults to None

    Returns:
        pd.DataFrame: New dataframe with calculated log columns
    """
    log_features: List[str] = kwargs.get("log_features", None)
    if log_features is not None:
        log_cols = [col + "_log" for col in log_features]
        df[log_cols] = np.log10(df[log_features].clip(lower=0) + 1)
    return df


def add_gradient_features(
    df: pd.DataFrame,
    **kwargs,
) -> pd.DataFrame:
    """
    Creates columns with gradient of curves. All created columns are suffixed with
    '_gradient'.

    Args:
        df (pd.DataFrame): dataframe with columns to calculate gradient from
    Keyword Args:
        gradient_features (list, optional): list of column names for the columns
            that gradient features should be calculated for. Defaults to None.

    Returns:
        pd.DataFrame: New dataframe with calculated gradient feature columns
    """
    gradient_features: List[str] = kwargs.get("gradient_features", None)
    if gradient_features is not None:
        gradient_cols = [col + "_gradient" for col in gradient_features]
        for i, feature in enumerate(gradient_features):
            df[gradient_cols[i]] = np.gradient(df[feature])
    return df


def add_rolling_features(
    df: pd.DataFrame,
    **kwargs,
) -> pd.DataFrame:
    """
    Creates columns with window/rolling features of curves. All created columns
    are suffixed with '_window_mean' / '_window_max' / '_window_min'.

    Args:
        df (pd.DataFrame): dataframe with columns to calculate rolling features from

    Keyword Args:
        rolling_features (list): columns to apply rolling features to. Defaults to None.
        depth_column (str): The name of the column to use to determine the sampling
            rate. Without this kwarg no rolling features are calculated.
        window (float): The window size to use for calculating the rolling
            features. **The window size is defined in distance**! The sampling rate
            is determined from the depth_column kwarg and used to transform the window
            size into an index based window. If this is not provided, no rolling features are calculated.

    Returns:
        pd.DataFrame: New dataframe with calculated rolling feature columns
    """
    rolling_features: List[str] = kwargs.get("rolling_features", None)
    window = kwargs.get("window", None)
    depth_column = kwargs.get("depth_column", None)
    if rolling_features is not None and window is not None and depth_column is not None:
        sampling_rate = utilities.calculate_sampling_rate(df[depth_column])
        window_size = int(window / sampling_rate)
        mean_cols = [col + "_window_mean" for col in rolling_features]
        df[mean_cols] = (
            df[rolling_features]
            .rolling(center=False, window=window_size, min_periods=1)
            .mean()
        )
        min_cols = [col + "_window_min" for col in rolling_features]
        df[min_cols] = (
            df[rolling_features]
            .rolling(center=False, window=window_size, min_periods=1)
            .min()
        )
        max_cols = [col + "_window_max" for col in rolling_features]
        df[max_cols] = (
            df[rolling_features]
            .rolling(center=False, window=window_size, min_periods=1)
            .max()
        )
    return df


def add_sequential_features(df: pd.DataFrame, **kwargs) -> pd.DataFrame:
    """
    Adds n past values of columns (for sequential models modelling). All created
    columns are suffixed with '_1' / '_2' / ... / '_n'.

    Args:
        df (pd.DataFrame): dataframe to add time features to

    Keyword Args:
        sequential_features (list, optional): columns to apply shifting to. Defaults to None.
        shift_size (int, optional): Size of the shifts to calculate. In other words, number of past values
            to include. If this is not provided, no sequential features are calculated.

    Returns:
        pd.DataFrame: New dataframe with sequential gradient columns
    """
    sequential_features: List[str] = kwargs.get("sequential_features", None)
    shift_size: int = kwargs.get("shift_size", None)
    if sequential_features and shift_size is not None:
        for shift in range(1, shift_size + 1):
            sequential_cols = [f"{c}_{shift}" for c in sequential_features]
            df[sequential_cols] = df[sequential_features].shift(periods=shift)
    return df


def add_petrophysical_features(df: pd.DataFrame, **kwargs) -> pd.DataFrame:
    """
    Creates petrophysical features according to relevant heuristics/formulas.

    The features created are as follows (each one can be toggled on/off via the
    'petrophysical_features' kwarg)::

        - VPVS = ACS / AC
        - PR = (VP ** 2 * 2 * VS ** 2) / (2 * (VP ** 2 * VS ** 2)) where
        - VP = 304.8 / AC
        - VS = 304.8 / ACS
        - RAVG = AVG(RDEP, RMED, RSHA), if at least two of those are present
        - LFI = 2.95 * ((NEU + 0.15) / 0.6) * DEN, and
            - LFI < *0.9 = 0
            - NaNs are filled with 0
        - FI = (ABS(LFI) + LFI) / 2
        - LI = ABS(ABS(LFI) * LFI) / 2
        - AI = DEN * ((304.8 / AC) ** 2)
        - CALI*BS = CALI * BS, where
            - BS is calculated using the guess_BS_from_CALI function from this
            module it is not found in the pass dataframe
        - VSH = Refer to the calculate_VSH docstring for more info on this

    Args:
        df (pd.DataFrame): dataframe to which add features from and to

    Keyword Args:
        petrophysical_features (list): A list of all the petrophysical features
            that should be created (see above for all the potential features
            this method can create). This defaults to an empty list (i.e. no
            features created).

    Returns:
        pd.DataFrame: dataframe with added features
    """
    petrophysical_features: List[str] = kwargs.get("petrophysical_features", None)

    if petrophysical_features is not None:
        # Calculate relevant features
        if "VP" in petrophysical_features:
            df = calculate_VP(df, **kwargs)

        if "VS" in petrophysical_features:
            df = calculate_VS(df, **kwargs)

        if "VPVS" in petrophysical_features:
            df = calculate_VPVS(df)

        if "PR" in petrophysical_features:
            df = calculate_PR(df)

        if "RAVG" in petrophysical_features:
            df = calculate_RAVG(df)

        if "LFI" in petrophysical_features:
            df = calculate_LFI(df)

        if "FI" in petrophysical_features:
            df = calculate_FI(df)

        if "LI" in petrophysical_features:
            df = calculate_LI(df)

        if "AI" in petrophysical_features:
            df = calculate_AI(df)

        if "CALI-BS" in petrophysical_features:
            df = calculate_CALI_BS(df)

        if "VSH" in petrophysical_features:
            df = calculate_VSH(df, **kwargs)

    return df


def add_well_metadata(df: pd.DataFrame, **kwargs) -> pd.DataFrame:
    """
    Adds well metadata columns to the provided dataframe from the provided
    well metadata dictionary (kwarg)

    Warning:
        This method will not work without the three kwargs listed below! It will
        return the df untouched and print a warning if kwargs are missing.

    Args:
        df (pd.DataFrame): The dataframe in which the well metadata columns will
            be added

    Keyword Args:
        metadata_dict (dict): The dictionary containing the relevant metadata
            per well (usually generated with the
            :py:meth: `get_well_metadata <akerbp.mlpet.utilties.get_well_metadata>` function).
        metadata_columns (list): List of metadata columns to add (each entry must
            correspond to a metadata key in the provided metadata_dict kwarg)
        id_column (str): The name of the column containing the well names (to be
            matched with the keys in the provided metadata_dict)

    Returns:
        pd.DataFrame: Return the passed dataframe with the requested columns added
    """
    id_column: str = kwargs.get("id_column", None)
    metadata_dict: Dict[str, Dict[str, Any]] = kwargs.get("metadata_dict", None)
    metadata_columns: List[str] = kwargs.get("metadata_columns", None)

    if not all([x is not None for x in [id_column, metadata_dict, metadata_columns]]):
        warnings.warn(
            "Could not add metadata because one of the necessary kwargs was "
            "missing! Returning the dataframe untouched."
        )
        return df

    # Reduce metadata dict to only desired columns
    mapper: Dict[str, Dict[str, Any]] = defaultdict(dict)
    for well, meta in metadata_dict.items():
        for k, v in meta.items():
            if k in metadata_columns:
                mapper[k][well] = v

    # Apply metadata mapping
    for column in metadata_columns:
        df[column] = df[id_column].map(mapper[column])

    return df


def add_formations_and_groups(
    df: pd.DataFrame,
    **kwargs,
) -> pd.DataFrame:
    """
    Adds a FORMATION AND GROUP column to the dataframe based on the well formation
    tops metadata and the depth in the column.

    Note:
        This function requires several kwargs to be able to run. If they are not
        provided a warning is raised and instead the df is returned untouched.

    Note:
        If the well is not found in formation_tops_mapping, the code will
        print a warning and continue to the next well.

    Example:
        An example mapper dictionary that would classify all depths in WELL_A
        between 120 & 879 as NORDLAND GP and all depths between 879 and 2014 as
        HORDALAND GP, would look like this::

            formation_tops_mapper = {
                "WELL_A": {
                    "labels": [NORDLAND GP, HORDALAND GP],
                    "levels": [120.0, 879.0, 2014.0]
                }
                ...
            }

        It can be generated by using the
        :py:meth: `get_formation_tops <akerbp.mlpet.utilties.get_formation_tops>` function

    Args:
        df (pd.DataFrame): The dataframe in which the formation tops label column
            should be added

    Keyword Args:
        id_column (str): The name of the column of well IDs
        depth_column (str): The name of the depth column to use for applying the
            mappings.
        formation_tops_mapper (dict): A dictionary mapping the well IDs to the
            formation tops labels, chronostrat and depth levels. For example::

                formation_tops_mapper = {
                    "31/6-6": {
                        "group_labels": ['Nordland Group', 'Hordaland Group', ...],
                        "group_labels_chronostrat": ['Cenozoic', 'Paleogene', ...]
                        "group_levels": [336.0, 531.0, 650.0, ...],
                        "formation_labels": ['Balder Formation', 'Sele Formation', ...],
                        "formation_labels_chronostrat": ['Eocene', 'Paleocene', ...],
                        "formation_levels": [650.0, 798.0, 949.0, ...]
                    }
                    ...
                }

            The above example would classify all depths in well 31/6-6 between 336 &
            531 to belong to the Nordland Group, and the corresponding chronostrat is the Cenozoic period.
            Depths between 650 and 798 are classified to belong to the Balder formation,
            which belongs to the Eocene period.
        client (CogniteClient): client to query CDF for formaiton tops if a mapping dictionary is not provided
            Defaults to None

    Returns:
        pd.DataFrame: dataframe with additional columns for FORMATION and GROUP
    """
    id_column: str = kwargs.get("id_column", None)
    depth_column: str = kwargs.get("depth_column", "DEPTH")
    formation_tops_mapper: Dict[
        str, Dict[str, Union[List[str], List[float]]]
    ] = kwargs.get("formation_tops_mapper", {})

    well_names = df[id_column].unique()
    if not formation_tops_mapper:
        try:
            formation_tops_mapper = utilities.get_formation_tops(
                well_names=well_names, client=kwargs["client"]
            )
        except KeyError as exc:
            raise ValueError(
                "Neither a formation tops mapping nor cognite client is provided. Not able to add formation tops to dataset"
            ) from exc
    df_ = df.copy()
    if id_column is not None and formation_tops_mapper:
        if depth_column not in df_.columns:
            raise ValueError(
                "Cannot add formations and groups metadata without a depth_column"
            )
        df_["GROUP"] = "UNKNOWN"
        df_["FORMATION"] = "UNKNOWN"

        for well in df_[id_column].unique():
            try:
                mappings = formation_tops_mapper[well]
            except KeyError:
                df_.loc[df_[id_column] == well, ["GROUP", "FORMATION"]] = np.nan
                warnings.warn(
                    f"No formation tops information found for {well}. Setting "
                    "both GROUP and FORMATION to NaN for this well."
                )
                continue

            group_labels, group_levels = (
                mappings["group_labels"],
                mappings["group_levels"],
            )
            formation_labels, formation_levels = (
                mappings["formation_labels"],
                mappings["formation_levels"],
            )

            if (len(group_levels) != len(group_labels) + 1) or (
                len(formation_levels) != len(formation_labels) + 1
            ):
                warnings.warn(
                    f"The formation top information for {well} is invalid! "
                    "Please refer to the docstring of this method to understand "
                    "the format in which formation top mappings should be provided."
                )
                continue

            well_df = df_[df_[id_column] == well]
            df_.loc[well_df.index, "GROUP"] = pd.cut(
                well_df[depth_column],
                bins=group_levels,
                labels=group_labels,
                include_lowest=True,
                right=False,
                ordered=False,
            )

            df_.loc[well_df.index, "FORMATION"] = pd.cut(
                well_df[depth_column],
                bins=formation_levels,
                labels=formation_labels,
                include_lowest=True,
                right=False,
                ordered=False,
            )
        df_["GROUP"] = utilities.map_formation_and_group(
            df_["GROUP"].astype(str).apply(utilities.standardize_group_formation_name)
        )[1]

        df_["FORMATION"] = utilities.map_formation_and_group(
            df_["FORMATION"]
            .astype(str)
            .apply(utilities.standardize_group_formation_name)
        )[0]

    else:
        raise ValueError(
            "A formation tops label could not be added to the provided dataframe"
            " because some keyword arguments were missing!"
        )
    return df_


def guess_BS_from_CALI(
    df: pd.DataFrame,
    standard_BS_values: List[float] = None,
) -> pd.DataFrame:
    """
    Guess bitsize from CALI, given the standard bitsizes

    Args:
        df (pd.DataFrame): dataframe to preprocess

    Keyword Args:
        standard_BS_values (ndarray): Numpy array of standardized bitsizes to
            consider. Defaults to::

                np.array([6, 8.5, 9.875, 12.25, 17.5, 26])

    Returns:
        pd.DataFrame: preprocessed dataframe

    """
    if standard_BS_values is None:
        standard_BS_values = [6, 8.5, 9.875, 12.25, 17.5, 26]
    BS_values = np.array(standard_BS_values)
    edges = (BS_values[1:] + BS_values[:-1]) / 2
    edges = np.concatenate([[-np.inf], edges, [np.inf]])
    df.loc[:, "BS"] = pd.cut(df["CALI"], edges, labels=BS_values)
    df = df.astype({"BS": np.float64})
    return df


def calculate_CALI_BS(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates CALI-BS assuming at least CALI is provided in the dataframe
    argument. If BS is not provided, it is estimated using the
    :py:meth:`guess_BS_from_CALI <akerbp.mlpet.feature_engineering.guess_BS_from_CALI>`
    method from this module.

    Args:
        df (pd.DataFrame): The dataframe to which CALI-BS should be added.

    Raises:
        ValueError: Raises an error if neither CALI nor BS are provided

    Returns:
        pd.DataFrame: Returns the dataframe with CALI-BS as a new column
    """
    if "CALI" in df.columns:
        if "BS" not in df.columns:
            df = guess_BS_from_CALI(df)
        df["CALI-BS"] = df["CALI"] - df["BS"]
    else:
        raise ValueError(
            "Not possible to generate CALI-BS. At least CALI needs to be present in the dataset."
        )

    return df


def calculate_AI(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates AI from DEN and AC according to the following formula::

        AI = DEN * ((304.8 / AC) ** 2)

    Args:
        df (pd.DataFrame): The dataframe to which AI should be added.

    Raises:
        ValueError: Raises an error if neither DEN nor AC are provided

    Returns:
        pd.DataFrame: Returns the dataframe with AI as a new column
    """
    if set(["DEN", "AC"]).issubset(set(df.columns)):
        df.loc[:, "AI"] = df["DEN"] * ((304.8 / df["AC"]) ** 2)
    else:
        raise ValueError(
            "Not possible to generate AI as DEN and AC are not present in the dataset."
        )
    return df


def calculate_LI(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates LI from LFI according to the following formula::

        LI = ABS(ABS(LFI) - LFI) / 2

    If LFI is not in the provided dataframe, it is calculated using the
    calculate_LFI method of this module.

    Args:
        df (pd.DataFrame): The dataframe to which LI should be added.

    Raises:
        ValueError: Raises an error if neither NEU nor DEN or LFI are provided

    Returns:
        pd.DataFrame: Returns the dataframe with LI as a new column
    """
    if "LFI" in df.columns:
        pass
    elif set(["NEU", "DEN"]).issubset(set(df.columns)):
        df = calculate_LFI(df)
    else:
        raise ValueError(
            "Not possible to generate LI as NEU and DEN or LFI are not present in dataset."
        )
    df["LI"] = abs(abs(df["LFI"]) - df["LFI"]) / 2
    return df


def calculate_FI(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates FI from LFI according to the following formula::

        FI = (ABS(LFI) + LFI) / 2

    If LFI is not in the provided dataframe, it is calculated using the
    calculate_LFI method of this module.

    Args:
        df (pd.DataFrame): The dataframe to which FI should be added.

    Raises:
        ValueError: Raises an error if neither NEU nor DEN or LFI are provided

    Returns:
        pd.DataFrame: Returns the dataframe with FI as a new column
    """
    if "LFI" in df.columns:
        pass
    elif set(["NEU", "DEN"]).issubset(set(df.columns)):
        df = calculate_LFI(df)
    else:
        raise ValueError(
            "Not possible to generate FI as NEU and DEN or LFI are not present in dataset."
        )
    df["FI"] = (df["LFI"].abs() + df["LFI"]) / 2
    return df


def calculate_LFI(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates LFI from NEU and DEN according to the following formula::

        LFI = 2.95 - ((NEU + 0.15) / 0.6) - DEN

    where:

        * LFI < -0.9 = 0
        * NaNs are filled with 0

    Args:
        df (pd.DataFrame): The dataframe to which LFI should be added.

    Raises:
        ValueError: Raises an error if neither NEU nor DEN are provided

    Returns:
        pd.DataFrame: Returns the dataframe with LFI as a new column
    """
    if set(["NEU", "DEN"]).issubset(set(df.columns)):
        df["LFI"] = 2.95 - ((df["NEU"] + 0.15) / 0.6) - df["DEN"]
        df.loc[df["LFI"] < -0.9, "LFI"] = 0
        df["LFI"] = df["LFI"].fillna(0)
    else:
        raise ValueError(
            "Not possible to generate LFI as NEU and/or DEN are not present in dataset."
        )
    return df


def calculate_RAVG(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates RAVG from RDEP, RMED, RSHA according to the following formula::

        RAVG = AVG(RDEP, RMED, RSHA), if at least two of those are present

    Args:
        df (pd.DataFrame): The dataframe to which RAVG should be added.

    Raises:
        ValueError: Raises an error if one or less resistivity curves are found
            in the provided dataframe

    Returns:
        pd.DataFrame: Returns the dataframe with RAVG as a new column
    """
    r_curves = [c for c in ["RDEP", "RMED", "RSHA"] if c in df.columns]
    if len(r_curves) > 1:
        df["RAVG"] = df[r_curves].mean(axis=1)
    else:
        raise ValueError(
            "Not possible to generate RAVG as there is only one or none resistivities curves in dataset."
        )
    return df


def calculate_VPVS(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates VPVS from ACS and AC according to the following formula::

        VPVS = ACS / AC

    Args:
        df (pd.DataFrame): The dataframe to which VPVS should be added.


    Raises:
        ValueError: Raises an error if neither ACS nor AC are found
            in the provided dataframe

    Returns:
        pd.DataFrame: Returns the dataframe with VPVS as a new column
    """
    if set(["AC", "ACS"]).issubset(set(df.columns)):
        df["VPVS"] = df["ACS"] / df["AC"]
    else:
        raise ValueError(
            "Not possible to generate VPVS as both necessary curves (AC and"
            " ACS) are not present in dataset."
        )
    return df


def calculate_PR(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates PR from VP and VS or ACS and AC (if VP and VS are not found)
    according to the following formula::

        PR = (VP ** 2 - 2 * VS ** 2) / (2 * (VP ** 2 - VS ** 2))

    where:

        * VP = 304.8 / AC
        * VS = 304.8 / ACS

    Args:
        df (pd.DataFrame): The dataframe to which PR should be added.

    Raises:
        ValueError: Raises an error if none of AC, ACS, VP or VS are found
            in the provided dataframe

    Returns:
        pd.DataFrame: Returns the dataframe with PR as a new column
    """
    if not set(["VP", "VS"]).issubset(set(df.columns)):
        if set(["AC", "ACS"]).issubset(set(df.columns)):
            df = calculate_VP(df)
            df = calculate_VS(df)
        else:
            raise ValueError(
                "Not possible to generate PR as none of the neccessary curves "
                "(AC, ACS or VP, VS) are present in the dataset."
            )
    df["PR"] = (df["VP"] ** 2 - 2.0 * df["VS"] ** 2) / (
        2.0 * (df["VP"] ** 2 - df["VS"] ** 2)
    )
    return df


def calculate_VP(df: pd.DataFrame, **kwargs) -> pd.DataFrame:
    """
    Calculates VP (if AC is found) according to the following formula::

        VP = 304.8 / AC

    Args:
        df (pd.DataFrame): The dataframe to which PR should be added.

    Raises:
        ValueError: Raises an error if AC is not found in the provided dataframe

    Returns:
        pd.DataFrame: Returns the dataframe with VP as a new column
    """
    if "AC" in df.columns:
        df["VP"] = 304.8 / df["AC"]
    else:
        raise ValueError("Not possible to generate VP as AC is not present in dataset.")
    return df


def calculate_VS(df: pd.DataFrame, **kwargs) -> pd.DataFrame:
    """
    Calculates VS (if ACS is found) according to the following formula::

        VS = 304.8 / ACS

    Args:
        df (pd.DataFrame): The dataframe to which PR should be added.

    Raises:
        ValueError: Raises an error if ACS is not found in the provided dataframe

    Returns:
        pd.DataFrame: Returns the dataframe with VS as a new column
    """
    if "ACS" in df.columns:
        df["VS"] = 304.8 / df["ACS"]
    else:
        raise ValueError(
            "Not possible to generate VS as ACS is not present in dataset."
        )
    return df


# VSH is a very complex function to disabling flake complexity check on this
def calculate_VSH(df: pd.DataFrame, **kwargs) -> pd.DataFrame:  # noqa: C901
    """
    Calculates the VSH curve based off the GR curve and the type of formation
    defined in the GROUP column, as follows::

        VSH = (GR - GR_ss) / (GR_sh_Gp_f - GR_ss)

    where:

        - GR_ss = The 5th quantile (quant_ss - value can be changed via the
            kwargs) of each defined system (some systems are grouped if relevant)
        - GR_sh_Gp_f = Shale formation groups are grouped by GROUP and a rolling
            window calculation is applied to each group (window size is
            determined by the 'window' kwarg and quantile is determined by
            the quant_sh kwarg - these default to 2500 and 0.95 respectively). A
            savgol filter of windowlength min(501, number_of_non_nans // 2)
            and polynomial order 3 is then applied to the rolling quantile group.
            Note that the filter is **ONLY** applied if there is enough non NaN
            data present in the rolling quantiles. This limit is currently set to
            10. If after this filter is applied the group still has np.NaNs, linear
            interpolation is applied to fill the gaps (provided there is data
            that can be used to interpolate). GR_sh_Gp_f represents
            this final result for all groups.

    Note:
        This calculation is performed **per well**! Formation tops column in input
        df is forced into upper case for generalization.

    Warning:
        If a calculation fails for one well, the well will be skipped and
        calculation continuous for the next well.

    Note:
        If no mapping could be made to the pre-defined systems, the GROUP will
        be labeled as 'other'.

    Args:
        df (pd.DataFrame): The dataframe to which VSH should be added.

    Keyword Args:
        groups_column_name (str): The name of the column containing
            group names. Defaults to 'GROUP'
        formations_column_name (str): The name of the column containing
            formation names. Defaults to 'FORMATION'
        id_column (str): The name of the well ID column to use for grouping
            the dataset by well. Defaults to 'well_name'
        rolling_window_size (int): The size of the window to use for the rolling quantile
            calculation of the shale formation groups. Defaults to 2000 or
            len(group_df) // 2 if less than 2000 where group_df is the dataframe
            for the specific shale formation group.
        filter_window_size (int): The size of the window to use for the savgol
            filtering. Defaults to 501 or odd(len(filter_series) // 2) if less
            than 501 where filter_series is the series of rolling quantiles to
            be filtered by the savgol filter. **MUST** be odd (if an even int is
            provided, the code automatically converts it to an odd window size)
        quant_ss (float): The quantile to use for each age group in the sand
            formation groups calculation (GR_ss). Defaults to 0.02
        quant_sh (float): The quantile to use in the rolling quantile calculation
            of the shale formation groups. Defaults to 0.95
        NHR_ss_threshold (float): The sand point threshold above which the
            Nordland, Hordaland & Rogaland (NHR) groups should be merged. The threshold
            is represented as the ratio between the group specific sandpoint
            (quant_ss) and the NHR system sand point (quant_ss calculated across all
            three groups - N, H & R). If this ratio is greater than this threshold
            the groups are merged according to the following strategy:

                1. Nordland's sandpoint is set to Hordaland's sandpoint. If there
                    is no Hordaland group present in the well it falls back to
                    being set to the NHR system sandpoint.
                2. Hordaland's sandpoint is set to the average of Nordland and
                    Rogaland's sandpoints
                3. Rogaland's sandpoint is set to Hordaland's sandpoint. If there
                    is no Hordaland group present in the well it falls back to
                    being set to the NHR system sandpoint.

        non_shale_window_threshold (float): A threshold for the following ratio::

                NSWT = GR_ss / (GR_sh_Gp_f * (GR_sh_Gp_f - GR_ss))

            This threshold causes the VSH_AUTO calculation to linearly interpolate
            between local minimas in the GR_sh_Gp_f curve whenever the above ratio
            goes above the user provided threshold. Initial user testing suggests
            a threshold of 0.015 is a good starting point.

    Returns:
        pd.DataFrame: Returns the dataframe with VSH as a new column
    """
    g_col: str = kwargs.get("groups_column_name", "GROUP")
    f_col: str = kwargs.get("formations_column_name", "FORMATION")
    rolling_window_size: int = kwargs.get("rolling_window_size", 2000)
    filter_window_size: int = kwargs.get("filter_window_size", 501)
    quant_ss: float = kwargs.get("quant_ss", 0.02)
    quant_sh: float = kwargs.get("quant_sh", 0.95)
    id_column: str = kwargs.get("id_column", "well_name")
    NHR_ss_threshold: float = kwargs.get("NHR_ss_threshold", 1.2)
    non_shale_window_threshold: float = kwargs.get("non_shale_window_threshold", 0.015)
    system_dict = {
        "Nordland": ["NORDLAND GP"],
        "Hordaland": ["HORDALAND GP"],
        "Rogaland": ["ROGALAND GP"],
        "preCretaceous": ["UNKNOWN GP"],
        "Cretaceous": ["SHETLAND GP", "CROMER KNOLL GP"],
        "Jurassic": [
            "VIKING GP",
            "TYNE GP",
            "BOKNFJORD GP",
            "FANGST GP",
            "BAT GP",
            "VESTLAND GP",
            "DUNLIN GP",
            "BRENT GP",
            "FLADEN GP",
        ],
    }
    mapping_dict = {val: key for key, lst in system_dict.items() for val in lst}

    def _calculate_VSH(df: pd.DataFrame) -> pd.DataFrame:
        # Reset index and preserve old one to be merged back later
        df = df.reset_index()
        old_index = df.pop("index")
        # Ensure only using legal GR values
        df.loc[df["GR"] < 0, "GR"] = np.nan
        # Calculate GR_ss
        df["Age"] = df[g_col].map(mapping_dict)
        # Where not defined in mapping_dict consider as other
        df.loc[df["Age"].isna(), "Age"] = "Other"
        system_quantiles = df.groupby("Age")["GR"].quantile(quant_ss)
        df["GR_ss"] = df["Age"].map(system_quantiles)
        # Need to ensure index is continuous after the groupby to prevent
        # different sections of the well being taken into account for the
        # calculation of quant_ss
        system_quantiles = {}
        for age, age_series in df.groupby("Age")["GR"]:
            # Ensure groups are continuous in index
            sub_ages = age_series.groupby(
                age_series.index.to_series().diff().ne(1).cumsum()
            )
            for i, sub_age_series in sub_ages:
                sub_age_name = f"{age}_{i}"
                df.loc[sub_age_series.index, "AGE_GROUPS"] = sub_age_name
                system_quantiles[sub_age_name] = sub_age_series.quantile(quant_ss)
        df["GR_ss"] = df["AGE_GROUPS"].map(system_quantiles)

        # Need to handle Nordland, Hordaland & Rogaland separetely (see docstring)
        nhr_quant_ss = df.loc[
            df[g_col]
            .str.upper()
            .str.contains("|".join(["NORDLAND", "ROGALAND", "HORDALAND"]), na=False),
            "GR",
        ].quantile(quant_ss)
        nord_quant_ss = system_quantiles.get("Nordland", np.nan)
        hord_quant_ss = system_quantiles.get("Hordaland", np.nan)
        roga_quant_ss = system_quantiles.get("Rogaland", np.nan)
        if not np.isnan(nord_quant_ss):
            if nord_quant_ss / nhr_quant_ss > NHR_ss_threshold:
                if not np.isnan(hord_quant_ss):
                    df.loc[df["Age"] == "Nordland", "GR_ss"] = hord_quant_ss
                else:
                    df.loc[df["Age"] == "Nordland", "GR_ss"] = nhr_quant_ss
        if not np.isnan(hord_quant_ss):
            if hord_quant_ss / nhr_quant_ss > NHR_ss_threshold:
                df.loc[df["Age"] == "Hordaland", "GR_ss"] = np.nanmean(
                    [nord_quant_ss, roga_quant_ss]
                )
        if not np.isnan(roga_quant_ss):
            if roga_quant_ss / nhr_quant_ss > NHR_ss_threshold:
                if not np.isnan(hord_quant_ss):
                    df.loc[df["Age"] == "Rogaland", "GR_ss"] = hord_quant_ss

        # Also need to handle draupne pseudo group separately
        # Make all groups in draupne formation have same GR_ss value from
        # the last group in the draupne formation
        if f_col is not None:
            mask = df[f_col].astype(str).str.contains("DRAUPNE").astype("boolean")
            groups_in_draupne = df.loc[mask, g_col].unique()
            if mask.sum() > 0 and len(groups_in_draupne) > 1:
                last_group = groups_in_draupne[-1]
                df.loc[mask, "GR_ss"] = df.loc[
                    df[g_col] == last_group, "GR_ss"
                ].unique()[0]

        # Calculate GR_sh_Gp_f
        for group_name, group_series in df.groupby(g_col, dropna=False, sort=False)[
            "GR"
        ]:
            # Ensure groups are continuous in index
            sub_groups = group_series.groupby(
                group_series.index.to_series().diff().ne(1).cumsum()
            )
            for i, sub_group_series in sub_groups:
                # First calculate the quantiles
                window_size = min(rolling_window_size, sub_group_series.size // 2)
                rolling_quantiles = sub_group_series.rolling(
                    window=window_size,
                    min_periods=min(100, window_size // 2),
                    center=True,
                ).quantile(quant_sh)
                # Then apply savgol_filter to non-nans
                non_nan_index = rolling_quantiles.notna()
                if non_nan_index.sum() > 10:
                    windowLength = min(
                        filter_window_size,
                        rolling_quantiles[non_nan_index].size // 2,
                    )
                    # windowLength must be odd so enforcing this below
                    windowLength += windowLength % 2 - 1
                    rolling_quantiles[non_nan_index] = savgol_filter(
                        rolling_quantiles[non_nan_index], windowLength, 3
                    )

                # Then linear interpolate if there are points that can be used to interpolate (i.e. non_nan values)
                if rolling_quantiles.notna().sum() > 0:
                    # Interpolate nan values using the index as x and curve as y
                    rolling_quantiles = rolling_quantiles.interpolate(
                        method="index", limit_direction="both"
                    )

                # Assign back to original df
                df.loc[rolling_quantiles.index, "GR_sh_Gp_f"] = rolling_quantiles
                if i == 1:
                    df.loc[rolling_quantiles.index, "INDEX_GROUPS"] = str(group_name)
                else:
                    df.loc[
                        rolling_quantiles.index, "INDEX_GROUPS"
                    ] = f"{group_name}_{i-1}"

        # Set curves to nan when GR is nan
        for curve in ["GR_ss", "GR_sh_Gp_f"]:
            df.loc[df["GR"].isna(), curve] = np.nan

        # Check for non-shale windows
        if non_shale_window_threshold is not None:

            # Define parameters to work with
            df["GR_sh_Gp_f_NS"] = df["GR_sh_Gp_f"].copy()
            df["VSH_AUT_INTER_RATIO"] = df["GR_ss"] / (
                df["GR_sh_Gp_f"] * (df["GR_sh_Gp_f"] - df["GR_ss"])
            )
            mask = df["VSH_AUT_INTER_RATIO"] >= non_shale_window_threshold

            # Define areas where non_shale_window_threshold was violated
            threshold_violations = utilities.get_violation_indices(mask)
            for _, row in threshold_violations.iterrows():
                # Check if well section contains a threshold violation
                # if not continue to next section
                start = row["first"]
                end = row["last"]
                groups = df.loc[start:end, "INDEX_GROUPS"].unique()
                # An index to determine whether to draw a vertical line
                # or interpolate with index - reset for each threshold violation
                vertical = np.nan
                if len(groups) == 1:
                    # Threshold violation applies to only one group so apply
                    # group specific logic
                    group = df.loc[df["INDEX_GROUPS"] == groups[0]].copy()
                    group_start = group.index[0]
                    group_end = group.index[-1]
                    if start == group_start and end == group_end:
                        # If the threshold violation applies for the entire group
                        # only, then just interpolate between before and after
                        # group. This accounts for step changes due to rolling window changes
                        if start == df.index[0]:  # start of the well
                            inter_start = group_start
                            inter_end = vertical = group_end + 1
                        elif end == df.index[-1]:  # end of the well
                            inter_start = vertical = group_start - 1
                            inter_end = group_end
                        else:
                            inter_start = group_start - 1
                            inter_end = group_end + 1
                    elif (end - start) / (group_end - group_start) > 0.5:
                        # If the threshold violation applies for the majority of the
                        # group attempt to reduce to sand point curve and recalculate
                        # the threshold violation length.
                        group["GR_ss"] = group["GR"].quantile(quant_ss / 2)
                        group["VSH_AUT_INTER_RATIO"] = group["GR_ss"] / (
                            group["GR_sh_Gp_f"] * (group["GR_sh_Gp_f"] - group["GR_ss"])
                        )
                        df.loc[group.index, "GR_ss"] = group["GR_ss"]
                        df.loc[group.index, "VSH_AUT_INTER_RATIO"] = group[
                            "VSH_AUT_INTER_RATIO"
                        ]
                        # Get new threshold start and end:
                        group_mask = (
                            group["VSH_AUT_INTER_RATIO"] >= non_shale_window_threshold
                        )
                        # If no more threshold violations then continue
                        if group_mask.sum() == 0:
                            continue

                        group_violations = utilities.get_violation_indices(group_mask)
                        inter_start, inter_end = [], []
                        for _, r in group_violations.iterrows():
                            start, end = r["first"], r["last"]
                            # Calculate inter_start and inter_end with inflection point
                            # algorithm
                            result = utilities.inflection_points(
                                df, "GR_sh_Gp_f", start, end
                            )
                            inter_start.append(result[0])
                            inter_end.append(result[1])

                        start_na = np.isnan(inter_start)
                        end_na = np.isnan(inter_end)
                        if start_na.any() and end_na.any():
                            inter_start = group_start - 1
                            inter_end = group_end + 1
                        elif start_na.any():
                            vertical = df.loc[inter_end, "GR_sh_Gp_f"].idxmax()
                            inter_start = group_start
                            inter_end = np.max(inter_end)
                        elif end_na.any():
                            inter_end = group_end
                            vertical = df.loc[inter_start, "GR_sh_Gp_f"].idxmax()
                            inter_start = np.min(inter_start)
                        else:
                            vertical = df.loc[
                                inter_start + inter_end, "GR_sh_Gp_f"
                            ].idxmax()
                            inter_start = np.min(inter_start)
                            inter_end = np.max(inter_end)
                    else:
                        inter_start, inter_end = utilities.inflection_points(
                            df, "GR_sh_Gp_f", start, end
                        )

                    # If only one inflection point, draw a vertical line
                    inter_mask = np.isnan([inter_start, inter_end])
                    if inter_mask.any():
                        if np.where(inter_mask)[0][0] == 0:
                            inter_start = group_start
                            vertical = inter_end
                        else:
                            inter_end = group_end
                            vertical = inter_start
                else:
                    # Threshold violation spans multiple groups. Just find
                    # start and end points for interpolation based purely
                    # on gradient changes
                    inter_start, inter_end = utilities.inflection_points(
                        df, "GR_sh_Gp_f", start, end
                    )

                    # If only one inflection point, draw a vertical line
                    inter_mask = np.isnan([inter_start, inter_end])
                    if inter_mask.any():
                        if np.where(inter_mask)[0][0] == 0:
                            inter_start = start
                            vertical = inter_end
                        else:
                            inter_end = end
                            vertical = inter_start

                # Bound indices to not go beyond the scope of the dataframe
                if inter_start < df.index[0]:
                    inter_start = df.index[0]
                if inter_end > df.index[-1]:
                    inter_end = df.index[-1]

                new_GR_sh_Gp_f = df.loc[inter_start:inter_end, "GR_sh_Gp_f_NS"].copy()
                # If vertical is not nan, it means we need to draw a vertical line
                if np.isnan(vertical):
                    new_GR_sh_Gp_f.iloc[1:-1] = np.nan
                    new_GR_sh_Gp_f = new_GR_sh_Gp_f.interpolate(method="index")
                else:
                    # Vertical should always be between inter_start and inter_end
                    vertical = np.clip(vertical, inter_start, inter_end)
                    new_GR_sh_Gp_f.loc[:] = new_GR_sh_Gp_f.loc[vertical]

                # Last check, if the new NS curve is less than the original
                # filtered rolling window curve then discard the interpolation
                original = df.loc[inter_start:inter_end, "GR_sh_Gp_f_NS"]
                check_mask = new_GR_sh_Gp_f < original
                if check_mask.sum() > 0:
                    new_GR_sh_Gp_f.loc[check_mask] = original

                # Assign back to original df
                df.loc[new_GR_sh_Gp_f.index, "GR_sh_Gp_f_NS"] = new_GR_sh_Gp_f

        # If after all this work the synthetic curves still have nans, no other choice than
        # to interpolate with ffill and bfill (only where GR is not na)
        curves = ["GR_ss"]
        if "GR_sh_Gp_f_NS" in df.columns:
            curves.append("GR_sh_Gp_f_NS")
        else:
            curves.append("GR_sh_Gp_f")
        for curve in curves:
            if df[curve].isna().sum() > 0:
                df[curve] = df[curve].interpolate(
                    method="index", limit_direction="both"
                )
        df.loc[df["GR"].isna(), curves] = np.nan

        # Finally put it all together
        if "GR_sh_Gp_f_NS" in df.columns:
            df["VSH"] = (df["GR"] - df["GR_ss"]) / (df["GR_sh_Gp_f_NS"] - df["GR_ss"])
        else:
            df["VSH"] = (df["GR"] - df["GR_ss"]) / (df["GR_sh_Gp_f"] - df["GR_ss"])
        df["VSH"] = df["VSH"].clip(lower=0, upper=1)
        # And remap the old index to restore df to original state
        df.index = df.index.map(old_index)

        # Drop unused columns
        df = df.drop(
            columns=[
                "Age",
                "GR_ss",
                "GR_sh_Gp_f",
                "GR_sh_Gp_f_NS",
                "VSH_AUT_INTER_RATIO",
                "INDEX_GROUPS",
                "AGE_GROUPS",
            ],
            errors="ignore",
        )

        return df

    # First check we have all necessary information
    required_cols = set(["GR", g_col, id_column])
    if f_col is not None:
        required_cols.add(f_col)
    provided_cols = set(df.columns)
    if not required_cols.issubset(provided_cols):
        raise ValueError(
            "Not possible to generate VSH as one or many of the necessary "
            f"columns {required_cols - provided_cols} are not present in the "
            "provided dataframe."
        )
    # Standardize g_col
    df[g_col] = utilities.map_formation_and_group(
        df[g_col].apply(utilities.standardize_group_formation_name)
    )[1]

    # If no formations_columns_name was provided, warn the user but continue
    if f_col is None:
        warnings.warn(
            "No formations_column_name was provided to the calculate_VSH "
            "function. It is therefore not possible to calculate VSH_AUTO with "
            "some custom formation mappings. The function will revert to using "
            " the groups_column_name provided but the calculated VSH_AUTO column"
            " will not be similar to the one generated in Techlog!"
        )
    else:  # Standardize f_col for later use
        df[f_col] = utilities.map_formation_and_group(
            df[f_col].apply(utilities.standardize_group_formation_name)
        )[0]

    # Process per well
    well_names = df[id_column].unique()
    dfs = []
    for well in well_names:
        well_df = df.loc[df[id_column] == well, :].copy()
        well_df = _calculate_VSH(well_df)
        dfs.append(well_df)
    df = pd.concat(dfs)

    return df


def add_vertical_depths(
    df: pd.DataFrame,
    **kwargs,
) -> pd.DataFrame:
    """Add vertical depths, i.e. TVDKB, TVDSS and TVDBML, to the input dataframe.
    This function relies on a keyword argument for a vertical depth mapper dictionary,
    created by querying CDF at discrete points along the wellbore for each well.
    To map the vertical depths along the entire wellbore, the data in the dictionary is interpolated by using the measured depth

    Args:
        df (pd.DataFrame): pandas dataframe to add vertical depths to

    Keyword Args:
        md_column (str): identifier for the measured depth column in the provided dataframe
            Defaults to None
        id_column (str): identifier for the well column in the provided dataframe
            Defaults to None
        vertical_depths_mapper (dict): dictionary containing vertical- and measured depths
            queried from CDF at discrete points along the wellbore for each well. For example::

                vertical_depths_mapper = {
                    "25/6-2": {
                        "TVDKB": [0.0, 145.0, 149.9998, ...],
                        "TVDSS": [-26.0, 119.0, 123.9998, ...],
                        "TVDBML": [-145.0, 0.0, 4.999799999999993, ...],
                        "MD": [0.0, 145.0, 150.0, ...]
                    }
                }

            Defaults to an empty dictionary, i.e. {}

        client (CogniteClient): client for querying vertical depths from CDF if a mapping dictionary is not provided
            Defaults to None

    Returns:
        pd.DataFrame: dataframe with additional column for TVDKB, TVDSS and TVDBML
    """
    md_column: str = kwargs.get("md_column", None)
    id_column: str = kwargs.get("id_column", None)
    client: CogniteClient = kwargs.get("client", None)
    vertical_depths_mapper: Dict[str, Dict[str, List[float]]] = kwargs.get(
        "vertical_depths_mapper", {}
    )
    well_names = df[id_column].unique()
    if len(vertical_depths_mapper) == 0:
        try:
            vertical_depths_mapper = utilities.get_vertical_depths(
                well_names=well_names, client=client
            )
        except AttributeError as exc:
            raise ValueError(
                "Neither a vertical depths mapping nor a cognite client is provided. Not able to add vertical depths to dataset"
            ) from exc
    if (
        md_column is not None
        and id_column is not None
        and len(vertical_depths_mapper) != 0
    ):
        df_ = df.copy()
        for well in vertical_depths_mapper:
            md_interpolate = df_.loc[df_[id_column] == well, md_column].to_list()
            depths = vertical_depths_mapper[well]
            md = depths["MD"]
            for key in depths.keys():
                if key == "MD":
                    continue
                vertical_depth = depths[key]
                with warnings.catch_warnings(record=True) as w:
                    f = interp1d(x=md, y=vertical_depth, fill_value="extrapolate")
                    interpolated_vertical_depth = f(md_interpolate)
                if w:
                    warnings.warn(
                        f"Interpolating {key} for well {well} triggered a "
                        f"runtime warning: {w[0].message}"
                    )
                df_.loc[df_[id_column] == well, key] = interpolated_vertical_depth
    else:
        raise ValueError(
            "The vertical depths could not be added to the provided dataframe"
            " because some keyword arugments were missing!"
        )
    return df_
