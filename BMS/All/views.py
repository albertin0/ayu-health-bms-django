import json

from django.shortcuts import render, HttpResponse
import bisect as b
import sqlite3
from datetime import datetime as dt
from django.views.decorators.csrf import csrf_exempt
import os.path

def create_conn():
    conn = None
    try:
        # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        BASE_DIR = '/Users/licious/Projects/practice_projects/ayu-health-bms-django/BMS'
        db_path = os.path.join(BASE_DIR, "db.sqlite3")
        conn = sqlite3.connect(db_path)
    except sqlite3.Error as e:
        print(e)
    return conn

# Create your views here.
def index(request):
    arr = [1,2,3,4,5,5]
    t = b.bisect(arr,4)
    return HttpResponse('This is Homepage!')

def view_movie(request,id):
    conn = create_conn()
    cur = conn.cursor()
    test = cur.execute(f'SELECT c.name, t.start_dt, t.end_dt FROM All_time t, All_cinema c where movie_id={id} AND t.cinema_id=c.id;')
    res = test.fetchall()
    print(len(res))
    response = []
    for r in res:
        c_name,st,end = tuple(r)
        print(st)
        temp = {
            "cinema_name":c_name,
            "start_time":st,
            "end_time":end
        }
        response.append(temp)
    return HttpResponse(f'{response}')

@csrf_exempt
def add_movie(request):
    # id = request.GET.get('id')
    # print(dt.now())
    # return HttpResponse(f'id:{id}')
    request = json.loads(request.body)
    print(request)
    name_m = request.get('name')
    c_list = request.get('cinema')
    details_m = request.get('details')
    conn = create_conn()
    cur = conn.cursor()
    q_m = "INSERT INTO All_movie (name,details) VALUES(?,?)"
    q_m2 = f'SELECT id FROM All_movie WHERE name="{name_m}"'

    cur.execute(q_m,(name_m, details_m))
    conn.commit()

    test = cur.execute(q_m2)
    res = test.fetchall()
    m_id = res[0][0]

    q_t = "INSERT INTO All_time (movie_id,cinema_id,start_dt,end_dt) VALUES(?,?,?,?)"
    for c in c_list:
        print(c)
        name, st, et = c['name'],c['start_time'],c['end_time']
        q_c = f'SELECT id FROM All_cinema WHERE name="{name}"'

        test = cur.execute(q_c)
        res = test.fetchall()
        c_id = res[0][0]

        cur.execute(q_t,(m_id,c_id,st,et))
        conn.commit()

    return HttpResponse('Movie ' + name_m + ' inserted into DB.')

def view_seats(request):
    c_id = request.GET.get('cinema_id')
    m_id = request.GET.get('movie_id')
    conn = create_conn()
    cur = conn.cursor()
    test = cur.execute(f'SELECT id FROM All_time WHERE movie_id={m_id} AND cinema_id={c_id};')
    test = test.fetchall()
    t_id = test[0][0]

    t2 = cur.execute(f'SELECT layout_id FROM All_cinema WHERE id={m_id}')
    t2 = t2.fetchall()
    l_id = t2[0][0]

    t3 = cur.execute(f'SELECT seat FROM All_layout WHERE layout_id={l_id}')
    t3 = t3.fetchall()
    total_seats = set([i[0] for i in t3])

    t_b = cur.execute(f'SELECT user_id, seat FROM All_booking WHERE time_id={t_id} AND status="C"')
    t_b = t_b.fetchall()
    booked = []
    b_set = set()
    for b in t_b:
        u_id, seat = tuple(b)
        t_u = cur.execute(f'SELECT name FROM All_user WHERE id={u_id}')
        t_u = t_u.fetchall()
        u_name = t_u[0][0]
        booked.append({
            "User_name":u_name,
            "Seat":seat
        })
        b_set.add(seat)
    avl_seats = total_seats - b_set
    avl_seats = list(avl_seats)
    avl = []
    for s in avl_seats:
        avl.append({
            "seat":s
        })
    res = "{" + "booked_seats:" + str(booked) + ", available_seats:" + str(avl) + "}"
    return HttpResponse(content=json.loads(json.dumps(res)))
    # print(len(test))
    # sol = ''
    # for row in test:
    #     a,b,c = tuple(row)
    #     sol += str(a) + ', ' + b + ', ' + str(c) + '.'
    # print(sol)
    # return HttpResponse('hello '+sol)

@csrf_exempt
def save_layout(request):
    conn = create_conn()
    cur = conn.cursor()
    test = cur.execute("select layout_id, group_concat(seat, ',') as seats from All_layout group by layout_id;")
    res = test.fetchall()
    layouts = []
    max_layout_id = 0
    for row in res:
        a0, a = tuple(row)
        max_layout_id = max(max_layout_id,a0)
        t = a.split(',')
        t.sort()
        print(t)
        layouts.append(t)
    print(layouts)
    print(str(request.POST.get('seats')).split(','))
    new_layout = str(request.POST.get('seats')).split(',')
    new_layout.sort()
    # if new_layout in layouts:
    #     return HttpResponse('Layout Already exists.-2')
    if new_layout not in layouts:
        max_layout_id+=1
        qry = '''insert into All_layout(layout_id, seat) values(?,?) '''
        for l in new_layout:
            print('adfagv-> ',l)
            t = (max_layout_id,str(l))
            cur.execute(qry,t)
            conn.commit()
        return HttpResponse('New Layout added. Id=' + str(max_layout_id) + ', and Layout=' + str(new_layout))
    return HttpResponse('Layout Already exists.')