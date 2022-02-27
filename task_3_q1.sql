--  Number of orders per month, total price of all those orders.

SELECT orderMonth, count(orderId), sum(SELECT price FROM product WHERE EXISTS(SELECT * FROM order_produt WHERE order_produt.orderID=order.id and order_produt.prductID=product.id))
FROM orders
GROUP BY orderMonth