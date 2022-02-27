--	For every product –
--      number of times was ordered,
--      number of customers who placed an order,
--      month with the max orders of this product.

SELECT *,
    count(SELECT orderId FROM order_product WHERE order_product.productID=product.id),
    count(SELECT id FROM customer WHERE EXISTS(SELECT * FROM order WHERE order.customerId=customer.id AND EXISTS(SELECT * FROM order_product WHERE order_product.productID=product.id AND order_product.orderID=order.id))),
    orderMonth FROM (SELECT max(count(orderID)), orderMonth FROM order_product JOIN order on orderID=order.id WHERE productID=product.id GROUP BY orderMonth)
FROM product