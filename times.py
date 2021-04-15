import datetime

def get_h_m_s(sec):
    td = datetime.timedelta(seconds=sec)
    m, s = divmod(td.seconds, 60)
    h, m = divmod(m, 60)

    if(h<1):
      if(m<1):
        seconds = str(s)+"秒"
        return seconds

      minutes = str(m)+"分"+str(s)+"秒"
      return minutes
    else:
      hours = str(h)+"時"+str(m)+"分"+str(s)+"秒"
      return hours