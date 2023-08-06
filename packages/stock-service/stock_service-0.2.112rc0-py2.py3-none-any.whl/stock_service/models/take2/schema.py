class Schema(dict):
    """
    Schema is a base class used to represent object entities like ProductStock.
    This has features like type and value validation, it also has dict and object
    representation.
    example:
        >>> stock = Schema(product_id=0, warehouse_id=0)
        >>> stock
        <Take2StockDict({'product_id': 0, 'warehouse_id': 10})>
        >>> stock.product_id, stock['product_id']
        (1, 1)
        >>> stock.product_id += 1
        >>> stock.product_id, stock['product_id']
        (2, 2)
    """

    def __repr__(self) -> str:
        return "<{}({})>".format(self.__class__.__name__, str(dict(self)))

    def __setattr__(self, name, value):
        self[name] = value

    def __getattr__(self, name):
        return self[name]

    def __setitem__(self, item, value: str):
        super().__setitem__(item, value)
