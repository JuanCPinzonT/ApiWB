import cx_Oracle
from django.utils import timezone

class Ingresar:
    def __init__(self):
        self.connection = cx_Oracle.connect("system", "pythonoracle", "localhost/XE")
    def consulta(self):
        cursor = self.connection.cursor()
        try:
            query = ("SELECT ID_CONSULTA, ID_USUARIO, FECHA_CONSULTA, DATOS_API FROM consultaapp")
            cursor.execute(query)
            resulatado = cursor.fetchall()
            return resulatado
        except cx_Oracle.Error as error:
            return f"Error: {str(error)}"
        finally:
            cursor.close()


    def insertar(self, id_consulta, id_usuario, titulo, descripcion, estado):
        cursor = self.connection.cursor()
        try:
            #convierte id_consulta a none si esta vacio
            id_consulta = None if not id_consulta else int(id_consulta)

            consulta = """
                            INSERT INTO propuestaApp (id_consulta, id_usuario, titulo, descripcion, fecha_creacion, estado)
                            VALUES (:1, :2, :3, :4, SYSDATE, :5)
                        """
            cursor.execute(consulta, (id_consulta, int(id_usuario), titulo, descripcion, estado))
            self.connection.commit()
            return f"Se ha ingresado: {cursor.rowcount} dato"
        except cx_Oracle.Error as error:
            return f"Error: {str(error)}"
        finally:
            cursor.close()

    def guardar_consulta(self, name, lastname, email, datos_api ):
        cursor = self.connection.cursor()
        try:
            query_user = ("INSERT INTO usuarioapp VALUES(seqcodigouser.nextval,:p1, :p2, :p3)")
            args_user = (name, lastname, email)
            cursor.execute(query_user, args_user)
            if cursor.rowcount > 0:
                dato = "user saved"
            else:
                dato = "The user has not been saved, try again"
            self.connection.commit()

            #Recoger el valor actual en ID_Usuario
            query_recoger_id_currval = ("SELECT seqcodigouser.currval FROM dual")
            id_usuario = cursor.execute(query_recoger_id_currval)
            for a, in id_usuario:
                dato1=a
            print(dato1)
            query_search =("INSERT INTO consultaapp (ID_CONSULTA,id_usuario,"
                           " FECHA_CONSULTA, DATOS_API) VALUES(seqconsultaapp.nextval,:p1, sysdate, :p5)")
            args_search = (dato1,datos_api)
            cursor.execute(query_search, args_search)
            if cursor.rowcount > 0:
                dato2 =  "Query saved"
            else:
                dato2 = "The query has not been saved, try again"

            self.connection.commit()

        except cx_Oracle.Error as error:
            return f"Error: {str(error)}"

        except self.connection.Error as error:
            print("Error: ", error)
        finally:
            cursor.close()
        return f"{dato}, {dato2}"
