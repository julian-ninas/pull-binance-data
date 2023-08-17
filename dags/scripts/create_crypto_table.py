
create_table_query = '''create table if not exists 
                        postgres.public.crypto_prices 
                            (crypto varchar,
                            open_time timestamp,
                            open float, 
                            high float, 
                            low float,
                            close float, 
                            volume float, 
                            close_time timestamp, 
                            quote_av float, 
                            trades int, 
                            tb_base_av float, 
                            tb_quote_av  float
                            )'''