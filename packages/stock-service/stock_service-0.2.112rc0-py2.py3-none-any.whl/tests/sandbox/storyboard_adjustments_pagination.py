import click
from datetime import datetime, timedelta
from pprint import pprint
from typing import Optional

from stock_client import StockServiceClient
from stock_service.config import Config

config = Config()
config.configure()

stock_client = StockServiceClient(endpoints=config.find_service("stock-service"))


def call_get_adjustments_by_filter(
    product_reference: str,
    location_id: int,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    start_adjustment_id: Optional[int] = None,
    end_adjustment_id: Optional[int] = None,
    page_size: Optional[int] = 10,
    output_filter: Optional[str] = None,
) -> dict:
    print(
        "Getting adjustments for "
        f"product_reference={product_reference} location_id={location_id} start_time={start_time} "
        f"end_time={end_time} start_adjustment_id={start_adjustment_id} "
        f"end_adjustment_id={end_adjustment_id} page_size={page_size}"
    )
    adjustments = stock_client.get_adjustments_by_filter(
        product_reference=product_reference,
        location_id=location_id,
        start_time=start_time,
        end_time=end_time,
        start_adjustment_id=start_adjustment_id,
        end_adjustment_id=end_adjustment_id,
        page_size=page_size,
    )
    if adjustments:
        if output_filter:
            pprint(
                [adjustment[output_filter] for adjustment in adjustments["adjustments"]]
            )
        else:
            pprint(adjustments["adjustments"])
    else:
        print("No adjustments found")


@click.command()
@click.option(
    "--output-filter",
    default=None,
    type=click.STRING,
    help="Filter all output by this key",
)
def main(output_filter: str):
    """
    Example usage:

    >>> python storyboard_adjustments_pagination.py
    [OrderedDict([('adjustment_id', 100),
              ('location_id', 1),
              ('product_reference', '1'),
              ('quantity', 10),
              ('old_adjustment_type_id', 4),
              ('old_adjustment_type_name', 'internal_allocation_adjustment'),
              ...

    >>> python storyboard_adjustments_pagination.py --output-filter adjustment_id
    [101, 100, ...]
    """
    product_reference = "90410519"
    location_id = 3
    today = datetime(
        year=2021, month=12, day=1, hour=0, minute=0, second=0, microsecond=0
    )
    yesterday = today - timedelta(days=1)

    # start_adjustment_id / start_time / end_time
    call_get_adjustments_by_filter(
        product_reference=product_reference,
        location_id=location_id,
        start_adjustment_id=100,
        start_time=yesterday,
        end_time=today,
        output_filter=output_filter,
    )

    # end_adjustment_id / start_time / end_time
    call_get_adjustments_by_filter(
        product_reference=product_reference,
        location_id=location_id,
        end_adjustment_id=108,
        start_time=yesterday,
        end_time=today,
        output_filter=output_filter,
    )

    # end_adjustment_id / start_time
    call_get_adjustments_by_filter(
        product_reference=product_reference,
        location_id=location_id,
        end_adjustment_id=108,
        start_time=yesterday,
        output_filter=output_filter,
    )

    # start_adjustment_id / end_time
    call_get_adjustments_by_filter(
        product_reference=product_reference,
        location_id=location_id,
        start_adjustment_id=108,
        end_time=today,
        output_filter=output_filter,
    )

    # start_time / end_time
    call_get_adjustments_by_filter(
        product_reference=product_reference,
        location_id=location_id,
        start_time=yesterday,
        end_time=today,
        output_filter=output_filter,
    )

    # start_time
    call_get_adjustments_by_filter(
        product_reference=product_reference,
        location_id=location_id,
        start_time=yesterday,
        output_filter=output_filter,
    )

    # end_time
    call_get_adjustments_by_filter(
        product_reference=product_reference,
        location_id=location_id,
        end_time=today,
        output_filter=output_filter,
    )

    # start_adjustment_id
    call_get_adjustments_by_filter(
        product_reference=product_reference,
        location_id=location_id,
        start_adjustment_id=100,
        output_filter=output_filter,
    )

    # end_adjustment_id
    call_get_adjustments_by_filter(
        product_reference=product_reference,
        location_id=location_id,
        end_adjustment_id=104,
        output_filter=output_filter,
    )

    # No filter
    call_get_adjustments_by_filter(
        product_reference=product_reference,
        location_id=location_id,
        output_filter=output_filter,
    )


if __name__ == "__main__":
    main()
