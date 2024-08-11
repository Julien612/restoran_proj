UPDATE restoran.order_list
SET order_list_status='$status'
where order_id=(select order_id from( select min(order_id) as order_id from restoran.order_list where order_list_status='type0') as a)