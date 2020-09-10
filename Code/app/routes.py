from flask import render_template, current_app
from app import app
from app import connection
import pandas as pd

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title = 'Global Terrorism Analysis')

@app.route('/trends')
def trends():
    return render_template('trends.html')

@app.route('/analysis')
def analysis():
    return render_template('analysis.html')


@app.route('/country')
def country():
    return render_template('country.html')


@app.route('/get_data_world')
def get_data_world():
    df = pd.read_sql("select iyear, count(eventid) as attacks, \
                    sum(case when nkill = '' then 0 else cast(nkill as int)  end) as deaths\
                    from main\
                    where success = '1'\
                    group by iyear", connection)
    
    return df.to_csv(index = False)


@app.route('/get_data_terrorist/<country>', methods=['GET'])
def get_data_terrorist(country):
    df = pd.read_sql("select count(eventid) as eventid, iyear, gname \
                        from main\
                        where country_txt = '" + country +"' and gname!= 'Unknown' \
                        group by iyear, gname", connection)
    year = 2011
    mask = (df['iyear'] > str(year))
    mask1 = (df['iyear'] <= str(year))
    df['group'] = ''
    df['group'][mask] = 'Active'
    df['group'][mask1] = 'Inactive'
    df1 = df[['gname','group','eventid']]
    df2 = df1.groupby(['gname','group'],as_index=False).eventid.count()
    df3 = df2.loc[df2['eventid'] > 2]
    
    return df3.to_csv(index = True)

@app.route('/get_data_aggregate/<country>', methods=['GET'])
def get_data_aggregate(country):
    df = pd.read_sql("select a.country_txt, a.attacks, a.deaths, a.wounds, b.successful_attacks, c.iyear, c.max_deaths  from \
                        (select country_txt, count(eventid) as attacks, \
                        sum(case when nkill = '' then 0 else cast(nkill as int)  end) as deaths,\
                        sum(case when nwound = '' then 0 else cast(nwound as int)  end) as wounds\
                        from main\
                       where country_txt = '" + country +"' \
                        group by country_txt) as a\
                        join\
                        (select count(eventid) as successful_attacks, country_txt\
                        from main\
                        where country_txt = '" + country +"' and success = '1'\
                        group by country_txt) as b\
                        on a.country_txt = b.country_txt\
                        join\
                        (select country_txt, iyear, \
                        sum(case when nkill = '' then 0 else cast(nkill as int)  end) as max_deaths\
                        from main\
                        where country_txt = '" + country +"' \
                        group by country_txt, iyear\
                        order by max_deaths desc\
                        limit 1) as c\
                        on b.country_txt = c.country_txt", connection)
    
    return df.to_json(orient = 'records')



@app.route('/get_data_top_cities/<country>', methods=['GET'])
def get_data_top_cities(country):
    df = pd.read_sql("select count(eventid) as num_attacks, \
                        sum(case when nkill = '' then 0 else cast(nkill as int)  end) as kills, city\
                        from main\
                        where country_txt = '" + country +"' \
                        group by city\
                        order by num_attacks desc\
                        limit 5", connection)
    return df.to_json(orient = 'records')

@app.route('/get_data_top_countries_deaths', methods=['GET'])
def get_data_top_countries_deaths():
    df = pd.read_sql("select sum(case when nkill = '' then 0 else cast(nkill as int)  end) as value, country_txt\
                        from main\
                        group by country_txt\
                        order by value desc\
                        limit 10", connection)
    return df.to_json(orient = 'records')

@app.route('/get_data_top_countries_attacks', methods=['GET'])
def get_data_top_countries_attacks():
    df = pd.read_sql("select count(eventid) as value, country_txt\
                        from main\
                        group by country_txt\
                        order by value desc\
                        limit 10", connection)

    return df.to_json(orient = 'records')

@app.route('/get_data_country_year_att_kills')
def get_data_country_year_att_kills():
    df = pd.read_sql("select count(eventid) as attacks, \
                        sum(case when nkill = '' then 0 else cast(nkill as int)  end) as kills, \
                        country_txt, iyear \
                        from main \
                        where success = '1' \
                        group by country_txt, iyear \
                        ", connection)
    df.loc[(df.country_txt == 'United States'), 'country_txt'] = 'USA'
    return df.to_csv(index = False)

@app.route('/get_csv_data')
def get_csv_data():
    df = pd.read_sql("select count(country_txt) as num_attacks, country_txt as name from main group by country_txt", connection)
    return df.to_csv(index = False)

@app.route('/get_csv_data_slider')
def get_csv_data_slider():
    df = pd.read_sql("select count(country_txt) as num_attacks, country_txt as name, iyear as iyear from main group by country_txt, iyear", connection)
    df.loc[(df.name == 'United States'), 'name'] = 'USA'
    return df.to_csv(index = False)

@app.route('/get_csv_data_dropdown', methods=['GET'])
def get_csv_data_dropdown():
    df = pd.read_sql("select sum(case when nkill = '' then 0 else cast(nkill as int)  end) as num_deaths, count(country_txt) as num_attacks, \
        country_txt as name, iyear as iyear  from main \
        where success = '1' \
        group by country_txt, iyear", connection)
    df.loc[(df.name == 'United States'), 'name'] = 'USA'
    return df.to_csv(index = False)

@app.route('/get_json_bar_race')
def get_json_bar_race():
    df = pd.read_sql("select count(country_txt) as num_attacks, country_txt, iyear as iyear  from main where success = '1' group by country_txt, iyear", connection)
    
    # print(df[(df['iyear'] == "2017")])
    # print(df[(df['iyear'] == "2017") & (df['country_txt'] == country)])

    data = {}
    country_list = df['country_txt'].unique()
    
    for year in range(1970,2018):
      temp = []
      year = str(year)
      temp_df = df[(df['iyear'] == year)]

      for country in country_list:
        temp_dict = {}
        temp_dict["country"] = str(country)
        # temp_df = df[(df['iyear'] == year) & (df['country_txt'] == country)]
        # temp_df.head()
        temp_country_df = temp_df[(temp_df['country_txt'] == country)]
        # print(temp_country_df)
        if not temp_country_df.empty:
          # print(temp_df['success'])
          temp_dict["value"] = int(temp_country_df['num_attacks'])
        else:
          temp_dict["value"] = 0
        temp.append(temp_dict)
      data[year] = temp

    return data


def cal_date(row):
  month = str(row['imonth'])
  if len(month) == 1:
    month ="0" + month
  date = str(row['iyear']) + "-" + month + "-" + "01"
  return date


@app.route('/get_csv_data_scatter/<int:year>')
def get_csv_data_scatter(year):
    df = pd.read_sql("select country_txt, longitude as long, latitude as lat, provstate, city, location, summary, attacktype1_txt, targtype1_txt, weaptype1_txt, motive, gname, iyear, scite1, imonth, iday, \
                    (case when nkill = '' then 0 else cast(nkill as int)  end) as kills,\
                    (case when nwound = '' then 0 else cast(nwound as int)  end) as wounds \
                    from main\
                    where success = '1' and iyear = '" + str(year) + "' and longitude != '' ", connection )

    return df.to_csv(index = False)

@app.route('/get_csv_world_scatter/<int:year>')
def get_csv_world_scatter(year):
    df = pd.read_sql("select country_txt, longitude as long, latitude as lat, provstate, city, location, summary, attacktype1_txt, targtype1_txt, weaptype1_txt, motive, gname, iyear, \
                    (case when nkill = '' then 0 else cast(nkill as int)  end) as kills,\
                    (case when nwound = '' then 0 else cast(nwound as int)  end) as wounds \
                    from main\
                    and success = '1' and iyear = '" + str(year) + "'and longitude != '' ", connection )

    return df.to_csv(index = False)


    
@app.route('/get_csv_data_terrorist/')
def get_csv_data_terrorist():


    df = pd.read_sql("select count(eventid) as num_attacks, gname, iyear\
                    from main\
                    where country_txt = 'United States' and success = '1'\
                    group by  gname, iyear;", connection)

    gname_list = df['gname'].unique()

    data = []
    for name in gname_list:
      n_df = df[df['gname'] == name]
      for y in range(1970,2018):
        y = str(y)
        y_df = n_df[n_df['iyear'] == y]
        val = 0
        if not y_df.empty:
          val = int(y_df['num_attacks'])
        temp_dict = {"gname":name,"year":y,"attacks":val}
        data.append(temp_dict)


@app.route('/get_csv_data_lineplot/<country>')
def get_csv_data_lineplot(country):

    df = pd.read_sql("select iyear , country_txt,\
                        count(eventid) as attacks,\
                        sum(case when nkill = '' then 0 else cast(nkill as int)  end) as kills,\
                        sum(case when nwound = '' then 0 when nwound = '8.5' then 8 else cast(nwound as int)  end) as wounds \
                        from main\
                        where country_txt = '" + country +"' \
                        group by iyear, country_txt\
                        order by iyear ", connection)

    return df.to_csv(index = False)


@app.route('/get_csv_attack_donutchart/<country>')
def get_csv_attack_donutchart(country):

    df = pd.read_sql("select count(eventid), attacktype1_txt,  country_txt\
                        from main \
                        where country_txt = '" + country +"' \
                        group by attacktype1_txt,  country_txt", connection)
                            # print(country)
    # print("Attack")
    # print(df)
    return df.to_csv(index = False)

@app.route('/get_csv_target_donutchart/<country>')
def get_csv_target_donutchart(country):

    df = pd.read_sql("select count(eventid), targtype1_txt,  country_txt\
                        from main \
                        where country_txt = '" + country +"' \
                        group by targtype1_txt,  country_txt", connection)
    # print("Target")
    # print(df)
    return df.to_csv(index = False)

@app.route('/get_csv_weapon_donutchart/<country>')
def get_csv_weapon_donutchart(country):

    df = pd.read_sql("select count(eventid), weaptype1_txt,  country_txt\
                        from main \
                        where country_txt = '" + country +"' \
                        group by weaptype1_txt,  country_txt", connection)

    # print("Weapon")
    # print(df)
    return df.to_csv(index = False)


