import main as m
import matplotlib.pyplot as plt
from os import mkdir
import time
start_time = time.time()


bd = m.PopulationData(name_file='bd.xls')
tbl = bd[0] + bd[1] + bd[2] # Выбираем базы данных (нужные таблицы)

tbl.limit_depth(0, 250) # Указываем глубину


kinds = tbl.get_kinds()
locals = tbl.get_locals()
for i in range(len(locals)):
    num_loc = i
    tbl_loc = tbl.limit_local(num_loc)

    name_dir = locals[num_loc]
    mkdir(name_dir)

    for num in range(len(kinds)-1):
        try:
            name = kinds[num] + '\n' + locals[num_loc]
            name_graph = kinds[num]
            tbl_kind = tbl_loc.limit_kind(num)

            res = tbl_kind.filter_columns([0, 7, 11])
            res.group_by_column([0, 1])
            res.group_date()
            if res.table.shape[0] < 4:
                continue
            res.plot([2])
            plt.title(name)
            plt.savefig(f'{name_dir}/{name_graph}.png')
            plt.close()
        except:
            pass


print("--- %s seconds ---" % (time.time() - start_time))
