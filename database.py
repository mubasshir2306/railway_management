from utils import get_connection
from datatypes import TrainDist, StationData, Train, Fares
from psycopg2 import sql


def show_all_trains(start: str, destination: str):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                DROP TABLE IF EXISTS starting;
                DROP TABLE IF EXISTS destination;
                CREATE TEMPORARY TABLE IF NOT EXISTS starting(
                    train_no INTEGER,
                    distance INTEGER,
                    departure_time TEXT
                );
                CREATE TEMPORARY TABLE IF NOT EXISTS destination(
                    train_no INTEGER,
                    distance INTEGER,
                    arrival_time TEXT
                );

                INSERT INTO starting(train_no, distance, departure_time)
                SELECT train_no, distance, departure_time FROM train_routes WHERE station_code = %s;

                INSERT INTO destination(train_no, distance, arrival_time)
                SELECT train_no, distance, arrival_time FROM train_routes WHERE station_code = %s;

                SELECT DISTINCT s.train_no, ti.train_name, s.departure_time, d.arrival_time,(d.distance-s.distance) 
                AS distance_bw_stations
                FROM starting AS s
                INNER JOIN destination AS d
                ON s.train_no = d.train_no
                INNER JOIN train_info AS ti
                ON s.train_no = ti.train_no
                WHERE (d.distance - s.distance > 0) 
                ORDER BY s.train_no;
                """, (start, destination)
            )
            res = cur.fetchall()

            if res:
                return [TrainDist(*t) for t in res]


def show_train_info(train_no: str):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT train_no, train_name, source_station_name, destination_station_name "
                        "FROM train_info WHERE train_no = %s;"
                        , (train_no,))
            res = cur.fetchall()

            if res:
                return [Train(*t) for t in res]


def get_fares(train_no: str, start: str, end: str):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                    SELECT tr1.train_no, ti.train_name,
                    (tr2.first_ac-tr1.first_ac) AS first_ac, 
                    (tr2.sec_ac-tr1.sec_ac) AS second_ac, 
                    (tr2.third_ac-tr1.third_ac) AS third_ac, 
                    (tr2.sleeper-tr1.sleeper) AS sleeper
                    FROM train_routes AS tr1
                    INNER JOIN train_routes AS tr2
                    ON tr1.train_no = tr2.train_no
                    INNER JOIN train_info AS ti
                    ON ti.train_no = tr1.train_no
                    WHERE tr1.train_no = %s AND tr2.station_code = %s AND tr1.station_code = %s
                """
                , (train_no, end, start))
            res = cur.fetchall()

            if res:
                return [Fares(*f) for f in res]


def get_station_code(station_name: str):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT DISTINCT station_code, station_name FROM train_routes WHERE station_name ILIKE %s"
                        "ORDER BY station_name;",
                        ('%' + station_name + '%',))
            res = cur.fetchall()
            if res:
                return [StationData(*s) for s in res]


def create_user(userid, fullname, mobileno, age, sex):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO users(userid, fullname, mobileno, age, sex) VALUES (%s, %s, %s, %s, %s);"
                        , (userid, fullname, mobileno, age, sex))


def check_if_exists(table, field, arg):
    table = str(table)
    field = str(field)
    arg = str(arg)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql.SQL("SELECT * FROM {} WHERE {} = {}").format(
                sql.Identifier(table),
                sql.Identifier(field),
                sql.Literal(arg)
            ))
            res = cur.fetchall()
            if res:
                return res


def delete_user(userid, mobileno):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM users WHERE userid = %s AND mobileno = %s;", (userid, mobileno))
