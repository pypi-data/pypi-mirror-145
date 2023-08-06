from datetime import datetime

from retry import retry
from sqlalchemy.exc import IntegrityError, OperationalError
from typing import Dict, Optional

from stock_client.constants import AdjustmentTypeNames
from stock_service.config import Config
from stock_service.controllers.stock_status_controller import get_stock_status_id
from stock_service.utils.stats import profile_with_stats
from stock_service.utils.tools import rounded_timestamp

config = Config()


@profile_with_stats(namespace="database.stock")
@retry(exceptions=OperationalError, tries=3, delay=0.1)
def create_adjustment(
    stock_id,
    old_adjustment_type_id,
    new_adjustment_type_id,
    quantity,
    levels,
    source_name="",
    source_reference="",
    source_timestamp=None,
    trace_id: Optional[str] = None,
    group_number: Optional[int] = None,
    sequence_number: Optional[int] = None,
):

    if source_timestamp is None:
        source_timestamp = rounded_timestamp()

    old_adjustment_type_id = int(old_adjustment_type_id)
    new_adjustment_type_id = int(new_adjustment_type_id)

    with config.db_client.get_connection("stock_primary") as connection:
        try:
            cursor = connection.execute(
                """
                INSERT INTO adjustment
                    (stock_id, old_adjustment_type_id, new_adjustment_type_id, quantity, source_name, source_reference,
                     source_timestamp, trace_id, group_number, sequence_number)
                VALUES
                    (%(stock_id)s, %(old_adjustment_type_id)s, %(new_adjustment_type_id)s, %(quantity)s,
                    %(source_name)s, %(source_reference)s, %(source_timestamp)s,
                    %(trace_id)s, %(group_number)s, %(sequence_number)s)
            """,
                {
                    "stock_id": stock_id,
                    "old_adjustment_type_id": old_adjustment_type_id,
                    "new_adjustment_type_id": new_adjustment_type_id,
                    "quantity": quantity,
                    "source_name": source_name,
                    "source_reference": source_reference,
                    "source_timestamp": source_timestamp,
                    "trace_id": trace_id,
                    "group_number": group_number,
                    "sequence_number": sequence_number,
                },
            )
        except IntegrityError:
            config.logger.exception(
                "create_adjustment_integrity_error, stock_id=%s, old_adjustment_type_id=%s, new_adjustment_type_id=%s",
                stock_id,
                old_adjustment_type_id,
                new_adjustment_type_id,
            )
            return 0

        adjustment_id = cursor.lastrowid

        for level in levels:
            status = level["status"]
            quantity = level["quantity"]
            stock_status_id = get_stock_status_id(status)
            connection.execute(
                """
                INSERT INTO adjustment_level
                    (adjustment_id, stock_status_id, quantity)
                VALUES
                    (%(adjustment_id)s, %(stock_status_id)s, %(quantity)s)
            """,
                {
                    "adjustment_id": adjustment_id,
                    "stock_status_id": stock_status_id,
                    "quantity": quantity,
                },
            )

    return adjustment_id


@profile_with_stats(namespace="database.stock")
def get_adjustment(adjustment_id):
    with config.db_client.get_connection("stock_primary") as connection:
        adjustment_result = connection.execute(
            """
            SELECT
                adjustment.adjustment_id,
                adjustment.source_timestamp,
                inventory.product_reference,
                stock.location_id,
                adjustment.quantity,
                adjustment.old_adjustment_type_id,
                adjustment.new_adjustment_type_id
            FROM
                adjustment
                INNER JOIN stock ON adjustment.stock_id = stock.stock_id
                INNER JOIN inventory ON stock.inventory_id = inventory.inventory_id
            WHERE
                adjustment_id = %(adjustment_id)s
        """,
            {"adjustment_id": adjustment_id},
        ).one_or_none()

        levels_result = connection.execute(
            """
            SELECT
                stock_status.status,
                adjustment_level.quantity
            FROM
                adjustment_level
                LEFT JOIN stock_status ON adjustment_level.stock_status_id = stock_status.stock_status_id
            WHERE
                adjustment_level.adjustment_id = %(adjustment_id)s
        """,
            {"adjustment_id": adjustment_id},
        ).fetchall()

        levels = [
            {"status": level["status"], "quantity": level["quantity"]}
            for level in levels_result
        ]

    response = {
        "adjustment_id": adjustment_id,
        "product_reference": adjustment_result["product_reference"],
        "source_timestamp": adjustment_result["source_timestamp"].timestamp(),
        "location_id": adjustment_result["location_id"],
        "quantity": adjustment_result["quantity"],
        "old_adjustment_type_id": adjustment_result["old_adjustment_type_id"],
        "new_adjustment_type_id": adjustment_result["new_adjustment_type_id"],
        "old_adjustment_type_name": AdjustmentTypeNames.get(
            adjustment_result["old_adjustment_type_id"], ""
        ),
        "new_adjustment_type_name": AdjustmentTypeNames.get(
            adjustment_result["new_adjustment_type_id"], ""
        ),
        "levels": levels,
    }

    return response


@profile_with_stats(namespace="database.stock")
def get_multiple_adjustments(
    product_reference: str,
    location_id: int,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    start_adjustment_id: Optional[int] = None,
    end_adjustment_id: Optional[int] = None,
    page_size: Optional[int] = 100,
) -> Dict:
    """
    Use the given filters to return multiple stock adjustments.

    :param location_id: get adjustments only for this location/warehouse ID
    :param product_reference: get adjustments only for this product reference
    :param start_time: adjustments will be no older than this time
    :param end_time: adjustments will be no newer than this time
    :param start_adjustment_id:
        IDs of adjustments will be no greater than this ID,
        indicates pagination to previous page of results
    :param end_adjustment_id:
        IDs of adjustments will be no less than this ID,
        indicates pagination to next page of results
    :param page_size: Max size of result set to return
    """
    with config.db_client.get_connection("stock_primary") as connection:
        sql_select_where = """
        SELECT
            adjustment.adjustment_id,
            adjustment.date_created,
            adjustment.source_timestamp,
            inventory.product_reference,
            stock.location_id,
            adjustment.quantity,
            adjustment.old_adjustment_type_id,
            adjustment.new_adjustment_type_id
        FROM
            adjustment
            INNER JOIN stock ON adjustment.stock_id = stock.stock_id
            INNER JOIN inventory ON stock.inventory_id = inventory.inventory_id
        WHERE
            inventory.product_reference = %(product_reference)s
            AND stock.location_id = %(location_id)s"""
        required_parameters = dict(
            product_reference=product_reference,
            location_id=location_id,
            page_size=page_size,
        )

        if start_adjustment_id and start_time and end_time:
            adjustment_results = connection.execute(
                f"""
                {sql_select_where}
                    AND adjustment.date_created >= %(start_time)s
                    AND adjustment.date_created <= %(end_time)s
                    AND adjustment.adjustment_id >= %(start_adjustment_id)s
                ORDER BY
                    adjustment.adjustment_id
                LIMIT
                    %(page_size)s
            """,
                dict(
                    required_parameters,
                    start_time=start_time,
                    end_time=end_time,
                    start_adjustment_id=start_adjustment_id,
                ),
            ).fetchall()[::-1]
        elif end_adjustment_id and start_time and end_time:
            adjustment_results = connection.execute(
                f"""
                {sql_select_where}
                    AND adjustment.date_created >= %(start_time)s
                    AND adjustment.date_created <= %(end_time)s
                    AND adjustment.adjustment_id <= %(end_adjustment_id)s
                ORDER BY
                    adjustment.adjustment_id DESC
                LIMIT
                    %(page_size)s
            """,
                dict(
                    required_parameters,
                    start_time=start_time,
                    end_time=end_time,
                    end_adjustment_id=end_adjustment_id,
                ),
            ).fetchall()
        elif start_adjustment_id and start_time:
            adjustment_results = connection.execute(
                f"""
                {sql_select_where}
                    AND adjustment.adjustment_id >= %(start_adjustment_id)s
                    AND adjustment.date_created >= %(start_time)s
                ORDER BY
                    adjustment.adjustment_id
                LIMIT
                    %(page_size)s
            """,
                dict(
                    required_parameters,
                    start_adjustment_id=start_adjustment_id,
                    start_time=start_time,
                ),
            ).fetchall()[::-1]
        elif end_adjustment_id and start_time:
            adjustment_results = connection.execute(
                f"""
                {sql_select_where}
                    AND adjustment.date_created >= %(start_time)s
                    AND adjustment.adjustment_id <= %(end_adjustment_id)s
                ORDER BY
                    adjustment.adjustment_id DESC
                LIMIT
                    %(page_size)s
            """,
                dict(
                    required_parameters,
                    start_time=start_time,
                    end_adjustment_id=end_adjustment_id,
                ),
            ).fetchall()
        elif start_adjustment_id and end_time:
            adjustment_results = connection.execute(
                f"""
                {sql_select_where}
                    AND adjustment.adjustment_id >= %(start_adjustment_id)s
                    AND adjustment.date_created <= %(end_time)s
                ORDER BY
                    adjustment.adjustment_id
                LIMIT
                    %(page_size)s
            """,
                dict(
                    required_parameters,
                    end_time=end_time,
                    start_adjustment_id=start_adjustment_id,
                ),
            ).fetchall()[::-1]
        elif end_adjustment_id and end_time:
            adjustment_results = connection.execute(
                f"""
                {sql_select_where}
                    AND adjustment.adjustment_id <= %(end_adjustment_id)s
                    AND adjustment.date_created <= %(end_time)s
                ORDER BY
                    adjustment.adjustment_id DESC
                LIMIT
                    %(page_size)s
            """,
                dict(
                    required_parameters,
                    end_time=end_time,
                    end_adjustment_id=end_adjustment_id,
                ),
            ).fetchall()
        elif start_time and end_time:
            adjustment_results = connection.execute(
                f"""
                {sql_select_where}
                    AND adjustment.date_created >= %(start_time)s
                    AND adjustment.date_created <= %(end_time)s
                ORDER BY
                    adjustment.adjustment_id DESC
                LIMIT
                    %(page_size)s
            """,
                dict(required_parameters, start_time=start_time, end_time=end_time),
            ).fetchall()
        elif start_time:
            adjustment_results = connection.execute(
                f"""
                {sql_select_where}
                    AND adjustment.date_created >= %(start_time)s
                ORDER BY
                    adjustment.adjustment_id DESC
                LIMIT
                    %(page_size)s
            """,
                dict(required_parameters, start_time=start_time),
            ).fetchall()
        elif end_time:
            adjustment_results = connection.execute(
                f"""
                {sql_select_where}
                    AND adjustment.date_created <= %(end_time)s
                ORDER BY
                    adjustment.adjustment_id DESC
                LIMIT
                    %(page_size)s
            """,
                dict(required_parameters, end_time=end_time),
            ).fetchall()
        elif start_adjustment_id:
            adjustment_results = connection.execute(
                f"""
                {sql_select_where}
                    AND adjustment.adjustment_id >= %(start_adjustment_id)s
                ORDER BY
                    adjustment.adjustment_id
                LIMIT
                    %(page_size)s
            """,
                dict(required_parameters, start_adjustment_id=start_adjustment_id),
            ).fetchall()[::-1]
        elif end_adjustment_id:
            adjustment_results = connection.execute(
                f"""
                {sql_select_where}
                    AND adjustment.adjustment_id <= %(end_adjustment_id)s
                ORDER BY
                    adjustment.adjustment_id DESC
                LIMIT
                    %(page_size)s
            """,
                dict(required_parameters, end_adjustment_id=end_adjustment_id),
            ).fetchall()
        else:
            adjustment_results = connection.execute(
                f"""
                {sql_select_where}
                ORDER BY
                    adjustment.adjustment_id DESC
                LIMIT
                    %(page_size)s
            """,
                dict(required_parameters),
            ).fetchall()

        response = {
            "page_size": page_size,
            "adjustments": [],
        }
        for adjustment_result in adjustment_results:
            levels_result = connection.execute(
                """
                SELECT
                    stock_status.status,
                    adjustment_level.quantity
                FROM
                    adjustment_level
                    LEFT JOIN stock_status ON adjustment_level.stock_status_id = stock_status.stock_status_id
                WHERE
                    adjustment_level.adjustment_id = %(adjustment_id)s
            """,
                {"adjustment_id": adjustment_result["adjustment_id"]},
            ).fetchall()

            levels = [
                {"status": level["status"], "quantity": level["quantity"]}
                for level in levels_result
            ]

            response["adjustments"].append(
                {
                    "adjustment_id": adjustment_result["adjustment_id"],
                    "date_created": adjustment_result["date_created"].isoformat(),
                    "product_reference": adjustment_result["product_reference"],
                    "source_timestamp": adjustment_result[
                        "source_timestamp"
                    ].timestamp(),
                    "location_id": adjustment_result["location_id"],
                    "quantity": adjustment_result["quantity"],
                    "old_adjustment_type_id": adjustment_result[
                        "old_adjustment_type_id"
                    ],
                    "new_adjustment_type_id": adjustment_result[
                        "new_adjustment_type_id"
                    ],
                    "old_adjustment_type_name": AdjustmentTypeNames.get(
                        adjustment_result["old_adjustment_type_id"], ""
                    ),
                    "new_adjustment_type_name": AdjustmentTypeNames.get(
                        adjustment_result["new_adjustment_type_id"], ""
                    ),
                    "levels": levels,
                }
            )

        return response

@profile_with_stats(namespace="database.stock")
def get_max_min_adjustmentids(
            product_reference: str,
            location_id: int,
            start_time: Optional[datetime] = None,
            end_time: Optional[datetime] = None,
    ) -> Dict:
        """
        Use the given filters to return multiple stock adjustments.

        :param location_id: get adjustments only for this location/warehouse ID
        :param product_reference: get adjustments only for this product reference
        :param start_time: adjustments will be no older than this time
        :param end_time: adjustments will be no newer than this time

        """
        with config.db_client.get_connection("stock_primary") as connection:
            required_parameters = dict(
                product_reference=product_reference,
                location_id=location_id,
            )

            if start_time:
                min_id = connection.execute(
                    """
                    SELECT
                        min(adjustment.adjustment_id)
                    FROM
                        adjustment
                        INNER JOIN stock ON adjustment.stock_id = stock.stock_id
                        INNER JOIN inventory ON stock.inventory_id = inventory.inventory_id
                    WHERE
                        inventory.product_reference = %(product_reference)s
                        AND stock.location_id = %(location_id)s
                        AND adjustment.date_created >= %(start_time)s
                """,
                    dict(required_parameters, start_time=start_time),
                ).fetchone()

            if end_time:
                max_id = connection.execute(
                    """
                    SELECT
                        max(adjustment.adjustment_id)
                    FROM
                        adjustment
                        INNER JOIN stock ON adjustment.stock_id = stock.stock_id
                        INNER JOIN inventory ON stock.inventory_id = inventory.inventory_id
                    WHERE
                        inventory.product_reference = %(product_reference)s
                        AND stock.location_id = %(location_id)s
                        AND adjustment.date_created >= %(end_time)s
                """,
                    dict(required_parameters, end_time=end_time),
                ).fetchone()

            response = {
                "max_id": max_id,
                "min_id": min_id,
            }

            return response

