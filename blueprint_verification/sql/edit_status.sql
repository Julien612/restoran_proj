UPDATE restoran.order_list
SET order_list_status='type1'
where order_id=(select order_id from( select max(order_id) as order_id from restoran.order_list where order_list_status='type3') as a) and dish_id='$dish_id'