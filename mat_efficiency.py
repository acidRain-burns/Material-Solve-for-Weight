import json, os, json_io

# module currently treats all goals as grams
# proper __name__ == __main__ coming soons

def update_obj(objects:dict):
    """Takes dictionary entries and adds missing values, returning a dictionary."""
    # Weight conversion will happen here eventually.
    for i in objects:
        eff = objects[i]['value']/objects[i]['weight']
        objects[i].update({'eff':eff})
        if objects[i]['qty'] > 0:
            objects[i].update({'has':True})
        else:
            objects[i].update({'has':False})
    return objects

def solve_weight(goal, obj:dict):
    progress = 0
    solve = dict(obj)
    solve_cost = 0
    print("\nWeight/Value Analysis")
    print(f"\nHomogenous Solutions - Goal: {goal}g")
    header = f"{'Item':^8} | {'Need/Have':>9} | {'Cost':^4} | {'$ per gram':<10} | {'Weight Each':^12}"
    print(header)
    for i in obj:
        req_qty = (goal/obj[i]['weight'])
        if req_qty%1 != 0:
            req_qty = int(req_qty)+1
        else:
            req_qty = int(req_qty)
        cost = (req_qty * obj[i]['value'])
        line = f"{req_qty:>3} /{obj[i]['qty']:>3}  | {cost:^4.2f} | {obj[i]['eff']:>10.3f} | {obj[i]['weight']:>8.2f} {obj[i]['weight_unit']}"
        print(f"{i.title():<8} | {line}")
    print(f"\nLeast Expensive Solution - Goal: {goal}g")
    while progress <= goal:
        key_min = min(solve.keys(), key=(lambda k: solve[k]['eff']))
        if solve[key_min]['has'] == True:
            need = goal - progress
            count_inc = int(need/solve[key_min]['weight'])
            if (need/solve[key_min]['weight'])%1 != 0:
                count_inc += 1
            if count_inc > solve[key_min]['qty']:
                count_inc = solve[key_min]['qty']
            weight_inc = count_inc * solve[key_min]['weight']
            progress = progress + weight_inc
            cost_inc = solve[key_min]['value']*count_inc
            solve_cost = solve_cost + cost_inc
            wu = solve[key_min]['weight_unit']
            w = solve[key_min]['weight']
            print(f"{key_min.title():<8}(s) x{count_inc:>3}, {weight_inc:>5.1f} {wu} @ {w:.1f} ea, ${cost_inc:>4.2f}")
            solve[key_min]['qty'] -= count_inc
            if solve[key_min]['qty'] <= 0:
                del solve[key_min]
        else:
            del solve[key_min]
    print(f"Final Price: ${solve_cost:>4.2f}")
    return solve

if __name__ == "__main__":
    objects_list = json_io.import_json('import_example.json')
    objects_list = update_obj(objects_list)
    remaining = solve_weight(200, objects_list)
    json_io.export_json(objects_list, file_path='', file_name='export_example', auto_rename=False)
    json_io.export_json(remaining, file_path='', file_name='remaining_example', auto_rename=False)