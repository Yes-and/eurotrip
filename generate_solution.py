from datetime import datetime, timedelta

def greedy_solution(data, initial_code="PRG"):
    path = [initial_code] # start at initial city
    fitness = 0 
    while True: # while we haven't visited all the cities
        destinations = data.loc[data["from.code"]==path[-1]].copy() # filter accessible destinations
        accessible = destinations.loc[~destinations["to.code"].isin(path)].copy() # remove visited destinations
        if accessible.shape[0]==0: # if we visited all destinations ...
            destinations = data.loc[data["from.code"]==path[-1]].copy()
            end_cost = destinations.loc[destinations["to.code"]==initial_code].copy()
            path.append(end_cost["to.code"].iloc[0]) # ... add the initial city ...
            fitness += end_cost["price.czk"].iloc[0] # ... and add fitness
            break
        min_cost = accessible.loc[accessible["price.czk"]==accessible["price.czk"].min()] # find cheapest destination from current destination ...
        path.append(min_cost["to.code"].iloc[0]) # ... and add it to the path ... 
        fitness += min_cost["price.czk"].iloc[0] # ... and the fitness
    return path, fitness

def greedy_solution_with_time(data, initial_code="PRG"):
    path = [initial_code]
    unique_destinations = len(list(data["from.code"].unique()))
    fitness = 0
    data["date"] = data["date"].apply(
        lambda x: datetime.strptime(x, "%Y-%m-%d").date()
        ) # make sure the date is in the correct format
    blacklist = {i:[] for i in sorted(data["date"].unique())}
    currdate = data.loc[data["from.code"]==initial_code]["date"].min() # add start date

    while True: # while we haven't visited all the cities
        if len(path)==unique_destinations: # if we visited all the cities
            end_cost = data.loc[
                (data["date"]==currdate) & (data["from.code"]==path[-1]) & (data["to.code"].isin([initial_code]))
            ].copy() # check that initial city is reachable ...
            if end_cost.shape[0]==0: # ... if not, add last city to blacklist ...
                blacklist[currdate - timedelta(days=1)].append(path.pop(-1))
                currdate -= timedelta(days=1)
                continue
            else: # ... else calculate cost to start city and end loop
                path.append(end_cost["to.code"].iloc[0])
                fitness += end_cost["price.czk"].iloc[0]
                break
        available_destinations = data.loc[
            (data["date"]==currdate) & (data["from.code"]==path[-1])
             ].copy() # filter destinations available from last destination on current date
        if available_destinations.shape[0] == 0:
            raise Exception(f"No destinations available from {path[-1]} on {currdate}")
        unvisited_destinations = available_destinations.loc[
            ~((available_destinations["to.code"].isin(path)) | (available_destinations["to.code"].isin(blacklist[currdate])))
            ].copy() # remove visited destinations and blacklisted destinations on said date ...
        if unvisited_destinations.shape[0]==0: # ... if there are none add start destination to blacklist on previous day ...
            blacklist[currdate - timedelta(days=1)].append(path.pop(-1))
            currdate -= timedelta(days=1)
            continue
        else: # ... else calculate minimal cost and select next destination
            min_cost = unvisited_destinations.loc[
                unvisited_destinations["price.czk"]==unvisited_destinations["price.czk"].min()
                ].copy()
            path.append(min_cost["to.code"].iloc[0])
            fitness += min_cost["price.czk"].iloc[0]
            currdate += timedelta(days=1) # shift date by 1 day

    print(blacklist)
    return path, fitness