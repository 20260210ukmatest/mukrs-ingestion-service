def __get_player_id(cur, ema_number, first_name, last_name):
    if ema_number:
        cur.execute(
            "select id from players where ema_number = %s;",
            [ema_number])
        player = cur.fetchone()
        if player:
            return player[0]

    cur.execute(
        "select id from players where first_name = %s and last_name = %s",
        (first_name, last_name)
    )
    player = cur.fetchone()
    if player:
        return player[0]
    return None

def __create_player(cur, first_name, last_name, country, ema_number):
    cur.execute(
        """insert into players (ema_number, first_name, last_name, country) 
        values (%s, %s, %s, %s) returning id""",
        (ema_number, first_name, last_name, country))
    return cur.fetchone()[0]

def __create_tournament(cur, tournament_info):
    cur.execute(
        """insert into tournaments (ema_id, name, place, country, date, players, mers_weight, mukrs_days) 
        values (%s, %s, %s, %s, %s, %s, %s, %s) returning id""",
        (tournament_info['ema_id'], tournament_info['name'], tournament_info['place'],
         tournament_info['country'], tournament_info['date'],
         tournament_info['players'], tournament_info['mers_weight'], tournament_info['mukrs_days'])
    )
    return cur.fetchone()[0]

def __insert_tournament_results(cur, tournament_id, player_base_ranks):
    for player in player_base_ranks:
        ema_number = player['ema_number']
        last_name = player['last_name']
        first_name = player['first_name']
        country = player['country']
        base_rank = player['base_rank']
        if base_rank == "-" or base_rank == "N/A":
            continue
        player_id = __get_player_id(cur, ema_number, first_name, last_name)
        if player_id is None:
            player_id = __create_player(cur, first_name, last_name, country, ema_number)
        cur.execute("""INSERT INTO tournament_results (tournament_id, player_id, base_rank) 
                            VALUES (%s, %s, %s)""",
                    (tournament_id, player_id, base_rank)
                    )
        
def save_tournament(cur, tournament_info, player_base_ranks):
    tournament_id = __create_tournament(cur, tournament_info)
    __insert_tournament_results(cur, tournament_id, player_base_ranks)