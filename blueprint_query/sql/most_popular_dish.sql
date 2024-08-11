select dish_name, dish_col , rep_gain
from restoran.rep_1
where rep_month='$input_month' and rep_year='$input_year' and dish_col=(select max(dish_col) from restoran.rep_1 where rep_month='$input_month' and rep_year='$input_year');

