SELECT dish_id, dish_name, dish_amount, order_id
FROM restoran.order_list join restoran.menu using(dish_id)
where order_id='$order_id' and order_list_status='type3'