import datetime, csv

class Horario:
    '''Horario de las monitorias y monitores.
    Conformado por un dia de la semana, una hora de inicio, y una hora de finalizacion'''
    def __init__(self, dia, horaInicio, horaFinal):
        self.dia = dia
        self.horaInicio = horaInicio
        self.horaFinal = horaFinal

class Monitoria:
    '''Monitoria completa, compuesta por una asignatura, un monitor, y un horario'''
    def __init__(self, materia, monitor, horario):
        self.materia = materia
        self.monitor = monitor
        self.horario = horario

class Monitor:
    '''Posible monitor.
    Conformado por un nombre, un diccionario de las materias a cuya monitoria aplica con su respectiva calificacion,
    y una lista de horarios disponibles'''
    def __init__(self, nombre, materias, horarios):
        self.nombre = nombre
        self.materias = materias
        self.horarios = horarios

class Materia:
    '''Materia que requiere de una monitoria.
    Conformada por el nombre de la materia, la cantidad de grupos de monitorias que necesitan ser creados, y una lista de posibles horarios'''
    def __init__(self, nombre, demanda, horarios):
        self.nombre = nombre
        self.demanda = demanda
        self.horarios = horarios

def stringAHoras(s):
    '''Metodo para transformar un string de tipo hh:mm a un objeto datetime.time'''
    horas = ""
    minutos = ""
    finalHoras = False
    for i in s:
        if i== ':':
            finalHoras = True
        elif finalHoras:
            minutos += i
        else:
            horas += i
    return datetime.time(int(horas), int(minutos))

def generarHorario(monitor, materia):
    '''Metodo para crear un nuevo horario basado en la posible interseccion de los horarios disponibles de un monitor y una materia.
    Si dicha interseccion no existe, el metodo retornara None. Se da por supuesto que las monitorias duraran 2 horas'''
    duracionMonitoria = 120
    for mat_horario in materia.horarios:
        for mon_horario in monitor.horarios:
            if mat_horario.dia == mon_horario.dia:
                if mat_horario.horaInicio < mon_horario.horaFinal and mon_horario.horaInicio < mat_horario.horaFinal:
                    horaInicioMonitoria = mat_horario.horaInicio if mon_horario.horaInicio < mat_horario.horaInicio else mon_horario.horaInicio
                    horaFinalMonitoria = mat_horario.horaFinal if mat_horario.horaFinal < mon_horario.horaFinal else mon_horario.horaFinal
                    if duracionMonitoria <= 60*(horaFinalMonitoria.hour - horaInicioMonitoria.hour) + horaFinalMonitoria.minute - horaInicioMonitoria.minute:
                        return Horario(mat_horario.dia, horaInicioMonitoria, datetime.time(horaInicioMonitoria.hour+2, horaInicioMonitoria.minute))
    return None

# Listas completas de materias, posibles monitores y monitorias del programa academico
materias = []
monitores = []
monitorias = []

# Obtencion de informacion del usuario
infomaterias = raw_input("Ingrese la direccion del archivo con la informacion de las materias del programa academico: ")
infomonitores = raw_input("Ingrese la direccion del archivo con la informacion de los posibles monitores: ")

# Creacion de la lista de materias
with open(infomaterias) as inf:
    archivo = csv.reader(inf)
    for materia in archivo:
        nombre = materia[0]
        demanda = int(materia[1])
        horarios = []
        for i in range(2, len(materia), 3):
            horarios.append(Horario(materia[i], stringAHoras(materia[i+1]), stringAHoras(materia[i+2])))
        materias.append(Materia(nombre, demanda, horarios))

# Creacion de la lista de monitores
with open(infomonitores) as inf:
    archivo = csv.reader(inf)
    for monitor in archivo:
        nombre = monitor[0]
        posiblesMaterias = {}
        horarios = []
        for i in range(1, 7, 2):
            if monitor[i] != None:
                posiblesMaterias[monitor[i]] = float(monitor[i+1])
        for j in range(7, len(monitor), 3):
            horarios.append(Horario(monitor[j], stringAHoras(monitor[j+1]), stringAHoras(monitor[j+2])))
        monitores.append(Monitor(nombre, posiblesMaterias, horarios))

print("Obtencion de informacion finalizada. A continuacion, se asignaran las monitorias con sus respectivos monitores y horarios.")

# Asignacion de monitores a cada materia
for mat in materias:
    monitoresAsignados = []
    for i in range(mat.demanda):
        horarioMonitoria = Horario("Monitoria no generada", datetime.time(0,0), datetime.time(0,0))
        posibleMonitor = Monitor("No se ha encontrado un monitor disponible para la asignatura",{},[])
        calificacionMax = 0
        for mon in monitores:
            if mat.nombre in mon.materias:
                if mon not in monitoresAsignados:
                    if mon.materias[mat.nombre] > calificacionMax:
                        posibleHorario = generarHorario(mon, mat)
                        if posibleHorario != None:
                            horarioMonitoria = posibleHorario
                            calificacionMax = mon.materias[mat.nombre]
                            posibleMonitor = mon
        monitorias.append(Monitoria(mat.nombre, posibleMonitor.nombre, horarioMonitoria))
        monitoresAsignados.append(posibleMonitor)

# Creacion del archivo de texto final
infomonitorias = raw_input("A continuacion podra guardar la informacion sobre las monitorias en un archivo de texto. Por favor ingrese la direccion completa y el nombre del archivo que sera creado: ")
with open(infomonitorias, "w") as archivo:
    salida = csv.writer(archivo)
    salida.writerow(["Materia", "Monitor", "Dia", "Hora de inicio", "Hora de finalizacion"])
    for monitoria in monitorias:
        salida.writerow([monitoria.materia, monitoria.monitor, monitoria.horario.dia, monitoria.horario.horaInicio, monitoria.horario.horaFinal])

print("Programa terminado.")