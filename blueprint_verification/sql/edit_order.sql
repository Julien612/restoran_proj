DELETE FROM restoran.check_order_list
WHERE check_id=(select min(check_id) from restoran.check_order) && dish_id != '$dish_id';