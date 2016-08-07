# -*- coding: utf-8 -*-
############################################################
# 假定站点编号从 1 ~ 10
# 共20节车厢, 每个车厢20排
# 编号形如
# 1A 1B 1C 1D 1F
# 2A 2B 2C 2D 2F
# ...
# 20A 20B 20C 20D 20F
# 20 * 5 * 20 = 2000个座位
# 其实座位编号完全可以从 0 ~ 1999, 并不影响我们对问题本身的分析
############################################################
import time

MAX_CARRIAGE_NUM = 20
MAX_ROW_NUM = 20
MAX_SITE_INDEX = 10


class Seg(object):
    def __init__(self, carriage_no, seat_no, start_site, end_site):
        # 车厢编号
        self.carriage_no = carriage_no
        # 座位编号
        self.seat_no = seat_no
        # 完整编号
        self.no = str(carriage_no) + '-' + seat_no
        # 能够售卖的开始站序号 int
        self.start_site = start_site
        # 能够售卖的终点站序号  int
        self.end_site = end_site

    def __str__(self):
        return str((self.no, self.start_site, self.end_site))


def init():
    ticket_dict = {}
    for i in range(1, MAX_SITE_INDEX):
        for j in range(i + 1, MAX_SITE_INDEX + 1):
            ticket_dict[(i, j)] = []

    for i in range(1, MAX_CARRIAGE_NUM + 1):
        for row in range(1, MAX_ROW_NUM + 1):
            for col in ['A', 'B', 'C', 'D', 'F']:
                # 每个座位都可以出售从s1 到 s10的车票
                key = (1, 10)
                # print Seg(i, str(row) + col, 1, 10)
                ticket_dict[key].append(Seg(i, str(row) + col, 1, 10))

    return ticket_dict


def sell(ticket_dict, start, end):
    '''

    :param ticket_dict:
    :param start:  购票的起始站
    :param end: 购票的终点站
    :return:
    '''
    # 需要找到一个有票的站点区间覆盖目标站点区间
    # 所有可能的起始站
    site_start = []
    x = 1
    while x <= start:
        site_start.append(x)
        x += 1
    site_start.reverse()

    # 所有可能的终点站
    site_end = []
    y = end
    while y <= MAX_SITE_INDEX:
        site_end.append(y)
        y += 1

    # print 'site_start', site_start
    # print 'site_end', site_end

    for x in site_start:
        for y in site_end:
            ticket = None
            if len(ticket_dict[(x, y)]) > 0:
                ticket = ticket_dict[(x, y)].pop()
            if ticket:
                # 判断一下这个座位的站点区间是否被完全用完了
                # 如果没有还需要把新生成的余票间存回去
                if start > x:
                    temp = Seg(ticket.carriage_no, ticket.seat_no, x, start)
                    ticket_dict[(x, start)].append(temp)
                if y > end:
                    temp = Seg(ticket.carriage_no, ticket.seat_no, end, y)
                    ticket_dict[(end, y)].append(temp)

                return Seg(ticket.carriage_no, ticket.seat_no, start, end)

    return None

def print_residual(ticket_dict):
    print '------------余票情况-------------'
    for key in ticket_dict:
        if ticket_dict[key]:
            print key, len(ticket_dict[key])

if __name__ == '__main__':
    ticket_dict = init()
    t1 = time.time()
    with open('req.csv') as fp:
        for line in fp:
            ll = line.split(',')
            user = ll[0]
            start = int(ll[1])
            end = int(ll[2])
            ticket = sell(ticket_dict, start, end)
            if ticket:
                print '#' * 100
                print line.strip()
                print user, "bought", ticket

            print_residual(ticket_dict)
            # time.sleep(2)
    t2 = time.time()
    print t2 - t1

