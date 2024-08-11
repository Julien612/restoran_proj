select dish_id, dish_name, dish_amount, order_id, order_date
from restoran.user_order join restoran.order_list using(order_id) join restoran.menu using(dish_id)
where order_list_status='done' and user_id='$user_id'
