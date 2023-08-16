import sqlite3 as sq

def get_product_list() -> list | str:
    try:
        con = sq.connect('db/mldc.db')
        cur = con.cursor()
        cur.execute('SELECT * FROM price_list')
        result = cur.fetchall()
        return result
    except sq.Error as err:
        err_text = f'Не удалось получить список номенклатуры из база данных. \n' \
                   f'{err}'
        return err_text


def set_new_price(price_id, price) -> None | str:
    try:
        con = sq.connect('db/mldc.db')
        cur = con.cursor()
        cur.execute('UPDATE price_list SET price = ? WHERE id = ?', (price, price_id,))
        con.commit()
    except sq.Error as err:
        err_text = f'Не удалось обновить цену в базе данных. \n' \
                   f'{err}'
        return err_text


def set_act_date(price_id, act_date) -> None | str:
    try:
        con = sq.connect('db/mldc.db')
        cur = con.cursor()
        cur.execute('UPDATE price_list SET act_date = ? WHERE id = ?', (act_date, price_id,))
        con.commit()
    except sq.Error as err:
        err_text = f'Не удалось обновить дату в базе данных. \n' \
                   f'{err}'
        return err_text


def check_act_date(act_date) -> bool | str:
    try:
        con = sq.connect('db/mldc.db')
        cur = con.cursor()
        cur.execute('SELECT count() FROM price_list WHERE act_date < ?', (act_date,))
        result = cur.fetchone()[0]
        if result == 0: return False
        else: return True
    except sq.Error as err:
        err_text = f'Не удалось получить список номенклатуры из база данных. \n' \
                   f'{err}'
        return err_text