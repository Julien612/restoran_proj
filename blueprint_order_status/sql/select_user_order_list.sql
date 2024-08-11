select order_id, dish_id, dish_name, dish_amount, order_list_status, order_bill, dish_price
from restoran.user_order join restoran.order_list using(order_id) join restoran.menu using(dish_id)
where user_id='$user_id' and order_list_status!='type0' and order_list_status!='done'
order by order_id