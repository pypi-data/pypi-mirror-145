import os

import cx_Oracle
import pandas as pd
import sqlalchemy
import cx_Oracle as ora
import sqlite3 as sq3
import psycopg2 as ps2
import mysql.connector as mysql
import pymssql as mssql
#from firebird.driver import driver_config as fbd, connect as fbdcnn
import fdb


# Reponsabilidades desta classe:
# Apenas se conectar a uma das bases de dados abaixo especificadas
# Bases conhecidas: SQLITE, ORACLE, MYSQL, POSTGRES, MSSQL, FIREBIRD, SQLCIPHER

class DATABASE:
    def __init__(self):
        self._connection_is_valid = True

    def ORACLE_SQLA(self, string_connect: dict):
        try:
            # Definindo a Library ORACLE
            if string_connect["path_library"] is None:
                pathlib = os.getenv("ORACLE_LIB")
            else:
                pathlib = string_connect["path_library"]

            # Consistindo se a biblioteca do oracle ja esta iniciada
            try:
                ora.init_oracle_client(lib_dir=pathlib)
            except:
                pass
                # não faz nada (e para deixar assim se nao da erro)
            # Validando se foi passado um driver para conexao
            if string_connect["driver_conexao"] is None:
                string_connect["driver_conexao"] = "cx_oracle"
            database = string_connect["database"]
            driver = string_connect["driver_conexao"]
            user = string_connect["username"]
            pwd = string_connect["password"]
            host = string_connect["host"]
            port = string_connect["port"]
            string_connect["instance"] = ora.makedsn(host, port, string_connect["instance"])
            # Validando o tipo de conexao (SID ou SERVICE_NAME) apenas oracle
            if string_connect["type_conection"].upper() == "SERVICE_NAME":
                string_connect["instance"] = string_connect["instance"].replace("SID", "SERVICE_NAME")
            dnsName = string_connect["instance"]
            str_cnn = f"""{database.lower()}{driver}://{user}:{pwd}@{dnsName}"""
            engine = sqlalchemy.create_engine(str_cnn)
            cnn = engine.connect()
            self._connection_is_valid = True
        except Exception as error:
            self._connection_is_valid = False
            cnn = error
        finally:
            return cnn

    def ORACLE(self, string_connect: dict):
        pathlib, cnn = None, None
        try:
            # Definindo a Library ORACLE
            if "library" in string_connect.keys():
                if string_connect["library"] is None:
                    pathlib = os.getenv("ORACLE_LIB")
                else:
                    pathlib = string_connect["library"]
            else:
                pathlib = os.getenv("ORACLE_LIB")

            # Consistindo se a biblioteca do oracle ja esta iniciada
            try:
                ora.init_oracle_client(lib_dir=pathlib)
            except:
                pass
                # não faz nada (e para deixar assim se nao da erro)

            # Definindo o tipo de instancia SID/SERVICE_NAME
            if string_connect["type_conection"].upper() == "SID":
                dnsName = ora.makedsn(host=string_connect["host"], port=string_connect["port"], sid=string_connect["instance"])
            else:
                dnsName = ora.makedsn(host=string_connect["host"], port=string_connect["port"], service_name=string_connect["instance"])

            # Efetuando a conexao com a instancia do BANCO
            cnn = ora.connect(string_connect["username"], string_connect["password"], dnsName, threaded=True)
        except Exception as error:
            msg = f"""Falha ao tentar se conectar com o banco de dados ORACLE [{string_connect["name_conection"]}].\nErro: {error} """
            cnn = msg
        finally:
            return cnn

    def SQLITE(self, database):
        DATABASE_NAME, result, msg, conn = None, False, None, None
        try:
            if os.path.isfile(database):
                cnn = sq3.connect(database)
                self._connection_is_valid = True
            else:
                msg = f"""SQLITE [{database}]- Não existe no local informado!"""
                raise Exception(msg)
        except Exception as error:
            cnn = error
            self._connection_is_valid = False
        finally:
            return cnn

    # ----------------------------------------------------------------
    # Falta driver
    def SQLCIPHER(self, database, password):
        DATABASE_NAME, result, msg, conn = None, False, None, None
        try:
            if os.path.isfile(database):
                #cnn = sqch.connect(database, password=password)
                self._connection_is_valid = True
            else:
                msg = f"""SQLITE [{database}]- Não existe no local informado!"""
                raise Exception(msg)
        except Exception as error:
            cnn = error
            self._connection_is_valid = False
        finally:
            return cnn

    def POSTGRES(self, string_connect: dict):
        msg, cnn = None, None
        try:
            # Efetuando a conexao com a instancia do BANCO
            cnn = ps2.connect(user=string_connect["username"], password=string_connect["password"], database=string_connect["instance"], host=string_connect["host"])
            self._connection_is_valid = True
        except Exception as error:
            cnn = f"""Falha ao tentar se conectar com o banco de dados POSTGRES.\n """
            self._connection_is_valid = False
        finally:
            return cnn

    def MSSQL(self, string_connect: dict):
        msg, cnn = None, None
        try:
            # Efetuando a conexao com a instancia do BANCO
            cnn = mssql.connect(user=string_connect["username"], password=string_connect["password"], database=string_connect["instance"], server=string_connect["host"])
            self._connection_is_valid = True
        except Exception as error:
            cnn = error
            self._connection_is_valid = False
        finally:
            return cnn

    def MYSQL(self, string_connect: dict):
        msg, cnn = None, None
        try:
            # Efetuando a conexao com a instancia do BANCO
            cnn = mysql.connect(user=string_connect["username"], password=string_connect["password"], database=string_connect["instance"], host=string_connect["host"])
            self._connection_is_valid = True
        except Exception as error:
            cnn = error
            self._connection_is_valid = False
        finally:
            return cnn

    # ----------------------------------------------------------------
    # Falta driver - maquina local não permite
    def FIREBIRD(self, string_connect: dict):
        msg, cnn = None, None
        try:
            user = string_connect["username"]
            pwd = string_connect["password"]
            host = string_connect["host"]
            port = string_connect["port"]
            instance = string_connect["instance"]
            cnn = fdb.connect(host=host, database=instance, user=user, password=pwd, port=port)
            self._connection_is_valid = True
        except Exception as error:
            cnn = error
            self._connection_is_valid = False
        finally:
            return cnn

    # ----------------------------------------------------------------
    # Falta tudo (Instalar driver ODBC) Maquina local não permite
    def INFORMIX(self, string_connect: dict):
        try:
            pass
            self._connection_is_valid = True
        except Exception as error:
            self._connection_is_valid = False
        finally:pass

    def METADATA(self,
                 conexao: object,
                 database: str,
                 nome_tabela: str,
                 alias: str = 'x',
                 quoted: bool = False,
                 rowid: bool = False,
                 join: str = None,
                 where: str = None,
                 orderby: str = None,
                 limit: int = 0
                 ) -> str:
        try:
            querys = {"ORACLE":   f"""Select * from all_tab_columns where table_name = '{nome_tabela}' order by column_id""""",
                      "POSTGRES": f"""Select * from information_schema.columns where table_name = '{nome_tabela}' order by ordinal_position""",
                      "SQLITE":   f"""Select * from pragma_table_info('{nome_tabela}') order by cid""",
                      "MYSQL":    f"""Select * from information_schema.columns where table_name = '{nome_tabela}' order by ordinal_position"""}
            qry = querys[database]
            df = pd.read_sql(con=conexao, sql=qry)
            nom_owner, column_list = None, []
            # OBTEM AS COLUNAS
            for index, row in df.iterrows():

                # -----------------------------------------
                # Banco SQLITE
                if database == "SQLITE":
                    column = df.loc[index, "name"]
                    # OWNER
                    nom_owner = ""
                    # QUOTED
                    if quoted:
                        column_list.append(f"""{alias}.\"{column}\"""")
                    else:
                        column_list.append(f"""{alias}.{column}""")
                # -----------------------------------------
                # Banco ORACLE
                elif database == 'ORACLE':
                    column = df.loc[index, "column_name"]
                    # QUOTED
                    if quoted:
                        column_list.append(f"""{alias}.\"{column}\"""")
                    else:
                        column_list.append(f"""{alias}.{column}""")
                    nom_owner = ""
                # Banco MYSQL
                elif database == "MYSQL":
                    column = df.loc[index, "column_name"]
                    # QUOTED
                    if quoted:
                        column_list.append(f"""{alias}.\"{column}\"""")
                    else:
                        column_list.append(f"""{alias}.{column}""")
                    # OWNER
                    nom_owner = ""
                # -----------------------------------------
                # Banco POSTGRES
                elif database == "POSTGRES":
                    column = df.loc[index, "column_name".lower()]
                    # QUOTED
                    if quoted:
                        column_list.append(f"""{alias}.\"{column}\"""")
                    else:
                        column_list.append(f"""{alias}.{column}""")
                    # OWNER
                    nom_owner = ""

            # ROWID
            if rowid:
                # -----------------------------------------
                # Banco SQLITE
                if database == "SQLITE":
                    column_list.append(f"""{alias}.ROWID ROWID_TABELA""")
                # -----------------------------------------
                # Banco ORACLE
                elif database == "ORACLE":
                    column_list.append(f"""rowidtochar({alias}.Rowid) "ROWID_TABELA" """)
                # -----------------------------------------
                # Banco MYSQL
                elif database == "MYSQL":
                    # não implementado
                    # tem que identificar qual a coluna do MYSQL que representa esta informação
                    pass
                # -----------------------------------------
                # Banco POSTGRES
                elif database == "POSTGRES":
                    column_list.append(f"""{alias}.row_number() OVER () ROWID_TABELA""")

            # Estruturando as colunas
            colunas = "\n      ,".join(column_list)
            select = f"""select {colunas}"""

            # NOME TABELA
            if quoted:
                tabela = f"""\n  from \"{nome_tabela.strip()}\" {alias.strip()}"""
            else:
                tabela = f"""\n  from {nome_tabela.strip()} {alias.strip()}"""

            # JOIN
            if join is None:
                join = ""
            else:
                join = f"""\n  {join}"""

            #WHERE
            if where is None:
                if database == "ORACLE" and limit > 0:
                    where = f"""\n where rownum <= {limit}"""
                else:
                    where = ""
            else:
                if database == "ORACLE" and limit > 0:
                    where = f"""\n {where.strip()}\n  and rownum <= {limit}"""
                else:
                    where = f"""\n {where.strip()}"""

            #ORDERBY
            if orderby is None:
                orderby = ""
            else:
                orderby = f"""\n {orderby.strip()}"""

            # LIMIT
            if database in ["MYSQL", "SQLITE", "POSTGRES"]:
                if limit > 0:
                    limit = f"""\nlimit {limit}"""
                else:
                    limit = ""
            else:
                limit = ""

            qry = f"""{select}{tabela}{join}{where}{orderby}{limit}""".lstrip()
            msg = qry
        except Exception as error:
            msg = error + qry
        finally:
            return msg

    @property
    def CONNECTION_VALID(self):
        return self._connection_is_valid

if __name__ == "__main__":
    pass
