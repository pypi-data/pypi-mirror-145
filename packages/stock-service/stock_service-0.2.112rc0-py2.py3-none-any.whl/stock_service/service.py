import click
from s4f import queue_pipeline_server, rpc_message_handler
import s4f.compiled_protobuffs.service_health_status_pb2 as health_pb
from s4f_clients.utils import protocolbuffer

from sqlalchemy.orm.exc import NoResultFound

from stock_client import stock_service_pb
from stock_client.constants import ErrorCodes

from stock_service.config import OldConfig
from stock_service.controllers.adjustment_controller import (
    get_adjustment,
    get_multiple_adjustments,
    get_max_min_adjustmentids,
)
from stock_service.controllers import service_health_controller
from stock_service.controllers import stock_adjustment_controller
from stock_service.controllers import stock_controller
from stock_service.controllers import stock_snapshot_controller
from stock_service.controllers import inventory_controller
from stock_service.errors import ServiceError
from stock_service.managers.update_stock_managers import adjust_stock_await
from stock_service.utils import stats
from stock_service.utils import tools


def run_service(port, workers: int):
    config = OldConfig()
    config.configure(db_pool_size=workers)

    logger = config.logger
    handler = rpc_message_handler.RpcMessageHandler(
        protobuf=stock_service_pb, stats_client=config.get_stats_client()
    )

    service = queue_pipeline_server.QueuePipelineServer(
        port=port,
        message_handler=handler,
        workers=workers,
        use_threads=True,
        http_health=True,
    )

    @handler.route("GetServiceHealth")
    @stats.profile_with_stats(namespace="s4f_endpoints")
    def get_service_health(request, version):
        response = health_pb.GetServiceHealthResponse()
        downstream_services_summary = (
            service_health_controller.get_downstream_services_status()
        )
        protocolbuffer.listfield_to_protocolbuffer(
            "test_results", downstream_services_summary, response
        )
        logger.info("health status: %s", str(response))
        return response

    @handler.route("GetStockOnHandForProducts")
    @stats.profile_with_stats(namespace="s4f_endpoints")
    def get_stock_on_hand_for_products_by_datetime(request, version):
        """
        returns the stock on hand for all given products in each warehouses using snapshot datetime

        :param products: list of product ids
        :param adjustment_datetime: adjustment timestamp to filter by
        """
        request_data = dict(protocolbuffer.protocolbuffer_to_dict(request))

        try:
            products_stock_on_hand = (
                stock_adjustment_controller.get_stock_on_hand_for_products(
                    request_data["product_ids"], request_data["adjustment_datetime"]
                )
            )
        except NoResultFound as err:
            raise ServiceError(ErrorCodes.NOT_FOUND, err._message)
        response = stock_service_pb.GetStockOnHandForProductsResponse()
        protocolbuffer.dict_to_protocolbuffer(
            dict(stock_hand_per_product=products_stock_on_hand), response
        )
        return response

    @handler.route("GetStockForWarehouses")
    @stats.profile_with_stats(namespace="s4f_endpoints")
    def get_stock_levels_for_warehouses(request, version):
        request_data = dict(protocolbuffer.protocolbuffer_to_dict(request))
        response = stock_service_pb.GetStockForWarehousesResponse()
        logger.info(
            "get_stock_levels_for_warehouses: getting stock for %s", request_data
        )
        products = stock_controller.get_stock_levels_for_warehouses(
            request_data.get("product_id"), request_data.get("warehouse_ids")
        )
        protocolbuffer.dict_to_protocolbuffer(dict(stock=products), response)
        return response

    @handler.route("GetStockLevels")
    @stats.profile_with_stats(namespace="s4f_endpoints")
    def get_stock_levels(request, version):
        request_data = protocolbuffer.protocolbuffer_to_dict(request)
        response = stock_service_pb.GetStockLevelsResponse()
        logger.info("get_stock_levels: getting stock for %s", dict(request_data))
        try:
            product_id, warehouse_id = (
                request_data["product_id"],
                request_data["warehouse_id"],
            )
            result = dict(
                stock=stock_controller.get_stock_levels(product_id, warehouse_id)
            )
        except NoResultFound:
            message = (
                "could not get stock level with product_id={}, warehouse_id={}".format(
                    product_id, warehouse_id
                )
            )
            logger.info(message)
            raise ServiceError(ErrorCodes.NOT_FOUND, message)

        protocolbuffer.dict_to_protocolbuffer(result, response)
        return response

    @handler.route("GetStockSnapshot")
    @stats.profile_with_stats(namespace="s4f_endpoints")
    def get_stock_snapshot(request, version):
        request_data = protocolbuffer.protocolbuffer_to_dict(request)
        logger.info(request_data)
        response = stock_service_pb.GetStockSnapshotResponse()
        stock_snapshot = stock_snapshot_controller.get_stock_snapshot(
            request_data["adjustment_id"]
        )
        result = {
            "adjustment_id": stock_snapshot["adjustment_id"],
            "snapshot": stock_snapshot,
        }
        logger.info(result)
        protocolbuffer.dict_to_protocolbuffer(result, response)
        return response

    @handler.route("CreateStockSnapshot")
    @stats.profile_with_stats(namespace="s4f_endpoints")
    def create_stock_snapshot(request, version):
        request_data = protocolbuffer.protocolbuffer_to_dict(request)
        logger.info(request_data)
        response = stock_service_pb.CreateStockSnapshotResponse()
        snapshot = stock_snapshot_controller.create_stock_snapshot(
            take2_adjustment_id=request_data["adjustment_id"],
            take2_snapshot=request_data["snapshot"],
        )
        protocolbuffer.dict_to_protocolbuffer(
            dict(snapshot=snapshot, adjustment_id=request_data["adjustment_id"]),
            response,
        )
        return response

    @handler.route("AdjustStock")
    @stats.profile_with_stats(namespace="s4f_endpoints")
    def adjust_stock(request, version):
        request_data = protocolbuffer.protocolbuffer_to_dict(request)
        response = stock_service_pb.AdjustStockResponse()
        logger.info("called adjust_stock with params: %s", dict(request_data))
        result = adjust_stock_await(
            request_data["product_id"],
            request_data["warehouse_id"],
            request_data["quantity"],
            request_data["old_reasoncode"],
            request_data["new_reasoncode"],
            request_data.get("customer_id"),
            request_data.get("instruction_id"),
            request_data.get("advanced_shipping_notification"),
            request_data.get("is_prepaid_voucher"),
            request_data.get("license_plate_number"),
            request_data.get("trace_id", str()),
            request_data.get("return_reference_number"),
            request_data.get("group_number", 0),
            request_data.get("sequence_number", 0),
        )
        protocolbuffer.dict_to_protocolbuffer(result, response)
        return response

    @handler.route("GetStockForWarehouseV2")
    @stats.profile_with_stats(namespace="s4f_endpoints")
    def get_stock_levels_v2(request, version):
        request_data = protocolbuffer.protocolbuffer_to_dict(request)
        product_reference, location_id = (
            request_data["product_id"],
            request_data["warehouse_id"],
        )
        try:
            levels = inventory_controller.get_stock_levels(
                owner_id=1, product_reference=product_reference, location_id=location_id
            )
        except NoResultFound:
            message = f"stock_not_found: product_reference={product_reference}, location_id={location_id}"
            logger.info(message)
            raise ServiceError(ErrorCodes.NOT_FOUND, message)

        result = {
            "product_id": product_reference,
            "warehouse_id": location_id,
            "stock_levels": levels,
        }

        response = stock_service_pb.GetStockForWarehouseV2Response()
        protocolbuffer.dict_to_protocolbuffer(data=result, message=response)
        return response

    @handler.route("GetStockForWarehousesV2")
    @stats.profile_with_stats(namespace="s4f_endpoints")
    def get_stock_levels_for_warehouses_v2(request, version):
        request_data = protocolbuffer.protocolbuffer_to_dict(request)
        product_reference, location_ids = (
            request_data["product_id"],
            request_data["warehouse_ids"],
        )

        result = list()

        for location_id in location_ids:
            try:
                levels = inventory_controller.get_stock_levels(
                    owner_id=1,
                    product_reference=product_reference,
                    location_id=location_id,
                )
            except NoResultFound:
                levels = []

            result.append(
                {
                    "product_id": product_reference,
                    "warehouse_id": location_id,
                    "stock_levels": levels,
                }
            )

        response = stock_service_pb.GetStockForWarehousesV2Response()
        logger.info(result)
        protocolbuffer.dict_to_protocolbuffer(
            data={"warehouse_stock": result}, message=response
        )
        return response

    @handler.route("SetStock")
    @stats.profile_with_stats(namespace="s4f_endpoints")
    def stock_sync_set_stock(request, version):
        request_data = protocolbuffer.protocolbuffer_to_dict(request)
        stock_service_pb.SetStockResponse()

        # Unpack the request
        request_data["trace_id"]
        old_format = dict(request_data["stock"])

        # Convert from legacy stock format to the new stock format
        new_format = tools.take2_stock_to_local_stock(old_format)

        # Use new format to update stock in "stock-service" DB
        logger.info("called stock_sync_set_stock with params: %s", new_format)
        raise NotImplementedError("stock_sync_set_stock")

    @handler.route("GetStockAdjustmentV2")
    @stats.profile_with_stats(namespace="s4f_endpoints")
    def get_adjustment_v2(request, version):
        request_data = protocolbuffer.protocolbuffer_to_dict(request)
        response = stock_service_pb.GetStockAdjustmentV2Response()
        adjustment = get_adjustment(adjustment_id=request_data["adjustment_id"])
        result = {"adjustment": adjustment}
        protocolbuffer.dict_to_protocolbuffer(result, response)
        return response

    @handler.route("GetFilteredStockAdjustments")
    @stats.profile_with_stats(namespace="s4f_endpoints")
    def get_adjustments_by_filter(request, version):
        request_data = protocolbuffer.protocolbuffer_to_dict(request)
        response = stock_service_pb.GetFilteredStockAdjustmentsResponse()
        result = get_multiple_adjustments(
            product_reference=request_data["product_reference"],
            location_id=request_data["location_id"],
            start_time=request_data.get("start_time", None),
            end_time=request_data.get("end_time", None),
            start_adjustment_id=request_data.get("start_adjustment_id", None),
            end_adjustment_id=request_data.get("end_adjustment_id", None),
            page_size=request_data.get("page_size", 100),
        )
        protocolbuffer.dict_to_protocolbuffer(result, response)
        return response

    @handler.route("GetFilteredStockAdjustments")
    @stats.profile_with_stats(namespace="s4f_endpoints")
    def get_max_min_adjustment_ids_by_filter(request, version):
        request_data = protocolbuffer.protocolbuffer_to_dict(request)
        response = stock_service_pb.GetFilteredStockAdjustmentsResponse()
        result = get_max_min_adjustmentids(
            product_reference=request_data["product_reference"],
            location_id=request_data["location_id"],
            start_time=request_data.get("start_time", None),
            end_time=request_data.get("end_time", None),
        )
        protocolbuffer.dict_to_protocolbuffer(result, response)
        return response

    service.serve()


@click.command()
@click.option("--port", default=9088, type=click.INT, help="Port to serve on")
@click.option("--workers", default=5, type=click.INT, help="Number of workers to start")
def serve(port, workers):
    run_service(port, workers)
