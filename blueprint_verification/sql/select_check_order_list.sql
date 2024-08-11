SELECT dish_id, dish_name, dish_amount, order_id
FROM restoran.order_list join restoran.menu using(dish_id)
where order_id=(select order_id from( select min(order_id) as order_id from restoran.order_list where order_list_status='type0') as a)