select sum(dish_price) from restoran.order_list join restoran.menu using(dish_id)
 where order_id='$order_id' and order_list_status='type1'