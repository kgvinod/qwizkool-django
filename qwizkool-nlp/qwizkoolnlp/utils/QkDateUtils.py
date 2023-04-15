import time
import random
import datetime
import dateparser

class QkDateUtils:
    """
    Date Utils for Qwizkool classes

    """

    def add_years(self, dt, years):
        try:
            #Return same day of the current year        
            return dt.replace(year = dt.year + years)
        except ValueError:
            #If same day not valid it will return another
            return dt + (date(dt.year + years, 1, 1) - date(dt.year, 1, 1))

    def add_months(self, dt, num_months):
        return dt + datetime.timedelta(days=num_months*30)

    def add_days(self, dt, num_days):
        return dt + datetime.timedelta(days=num_days)

    def generate_similar_year(self, dt, max_range):
        
        incr = random.randint(1, max_range)
            
        # random add/subtract
        mult = 1
        if bool(random.getrandbits(1)):
            mult *= -1

        incr *= mult
        dt_updated = self.add_years(dt, incr)
        
        # if this is a future date, generate all dates in future
        if dt > datetime.datetime.now():        
            # If date went into the past, generate one in the future
            if dt_updated < datetime.datetime.now():
                dt_updated = self.add_years(dt, -1*incr)
        else:
            # If date went into the future, generate one in the past
            if dt_updated > datetime.datetime.now():
                dt_updated = self.add_years(dt, -1*incr)
                
        return dt_updated


    def generate_similar_month(self, dt, max_range):
        
        incr = random.randint(1, max_range)
            
        # random add/subtract
        mult = 1
        if bool(random.getrandbits(1)):
            mult *= -1

        incr *= mult
        dt_updated = self.add_months(dt, incr)
        
        # if this is a future date, generate all dates in future
        if dt > datetime.datetime.now():        
            # If date went into the past, generate one in the future
            if dt_updated < datetime.datetime.now():
                dt_updated = self.add_months(dt, -1*incr)
        else:
            # If date went into the future, generate one in the past
            if dt_updated > datetime.datetime.now():
                dt_updated = self.add_months(dt, -1*incr)
                
        return dt_updated

    def generate_similar_day(self, dt, max_range):
        
        incr = random.randint(1, max_range)
            
        # random add/subtract
        mult = 1
        if bool(random.getrandbits(1)):
            mult *= -1

        incr *= mult
        dt_updated = self.add_days(dt, incr)
        
        # if this is a future date, generate all dates in future
        if dt > datetime.datetime.now():        
            # If date went into the past, generate one in the future
            if dt_updated < datetime.datetime.now():
                dt_updated = self.add_days(dt, -1*incr)
        else:
            # If date went into the future, generate one in the past
            if dt_updated > datetime.datetime.now():
                dt_updated = self.add_days(dt, -1*incr)
                
        return dt_updated

    def get_similar_dates(self, date_str, count):

        ret = dict()
        ret['answer'] = ''
        ret['choices'] = []

        datetimes = []
        date_format_str = ''
        
        # dateparser does not tell which date parts were specified
        # So use two different base settings to figure out which ones were
        date_settings={'RELATIVE_BASE': datetime.datetime(1800, 12, 12)}
        print('Date String=', date_str)

        date1 = None
        
        try:
            date1 = dateparser.parse(date_str, settings=date_settings)
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
        
        if date1 is None:
            #print("Don't know how to handle date", date_str)
            return ret
        
        date_settings={'RELATIVE_BASE': datetime.datetime(1900, 1, 1)}
        date2 = dateparser.parse(date_str, settings=date_settings)
            
        day_specified = date1.day == date2.day   
        if day_specified:
            date_format_str += '%d '
            
        month_specified = date1.month == date2.month    
        if month_specified:
            date_format_str += '%b '    
        
        year_specified = date1.year == date2.year
        if year_specified:
            date_format_str += '%Y '
        
        time_specified = date1.hour != 0 or date1.minute != 0 or date1.second != 0    
        if time_specified:
            date_format_str += '%H:%M:%S '
            
        if day_specified:
            while (True):
                new_date = self.generate_similar_day(date1, 60)
                if new_date not in datetimes:
                    datetimes.append(new_date)
                if len(datetimes) >= count:
                    break
        elif month_specified:
            while (True):
                new_date = self.generate_similar_month(date1, 24)
                if new_date not in datetimes:
                    datetimes.append(new_date)
                if len(datetimes) >= count:
                    break
        elif year_specified:
            while (True):
                new_date = self.generate_similar_year(date1, 20)
                if new_date not in datetimes:
                    datetimes.append(new_date)
                if len(datetimes) >= count:
                    break

        ret['answer'] = date1.strftime(date_format_str).strip()
        for dt in datetimes:
            ret['choices'].append(dt.strftime(date_format_str).strip())

        #print("Created date choices", date_str, ret['answer'], ret['choices'])    
        return ret