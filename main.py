import numpy
import pandas as pd

PartitionSize=pd.read_csv("Data/size.csv")
PartitionList= PartitionSize["Size"].values.tolist()
WaitingList=[]
AvailabilityList=[True,True,True,True,True,True,True]
PrincipalMemory=[None,None,None,None,None,None,None,None]
FinishedProcesses=[]

MemoryProcessCount=[]



def main_menu():
    print("Simulador de Ingreso de procesos en una memoria principal particionada")
    print("1. Imprimir proceso: ")
    print("2. Ingresar proceso: ")
    print("3. Mostrar proceso: ")
    print("4. Sacar proceso: ")
    print("5. Terminar: ")

    opcion= input("Seleccione una opcion del 1 al 5: ")

    if opcion == '1':
        PrintMemoryState(PartitionList,AvailabilityList)
        print("------------------------------------------")
        main_menu()
    elif opcion == '2':
        ProcessInput(AvailabilityList,PartitionList)
        print("------------------------------------------")
        main_menu()

    elif opcion == '3':
        ShowWaitinListProcesses()
    elif opcion == '4':
        RemoveProcess()
    elif opcion == '5':
        FinishedProcesses()
    else:
        print("Opción invalida, Por Favor seleccione un numero del 1 al 5")
        main_menu()



def PrintMemoryState(PartitionList,AvailabilityList):
    DataTuple=list(zip(PartitionList,AvailabilityList))
    df=pd.DataFrame(DataTuple,columns=["PartitionList","AvailabilityList"])
    print(df)
    return df


def CheckAvailability(ProcessAvailability):
    AvailabilityIndexes=[index for (index,item) in enumerate(ProcessAvailability) if item ==True]
    return AvailabilityIndexes



def CheckSize(AvailableList,PartitionListSize,ProcessSize):
    FilteredElements = [PartitionListSize[i] for i in AvailableList]
    FilteredElements =[item - ProcessSize for item in FilteredElements]

    SizeListDiffDict=dict(zip(AvailableList,FilteredElements))

    SizeListDiffDict = {key: value for key, value in SizeListDiffDict.items() if value >= 0}

    if len(SizeListDiffDict)<=0:
        print("Necesitas liberar un espacio para introducir el proceso")
        return None

    else:
        min_key = min(SizeListDiffDict, key=lambda k: SizeListDiffDict[k])
        min_value = SizeListDiffDict[min_key]
        return min_key




def ProcessInput(AvailabilityList,PartitionList):

    ProcessName= input("Ingrese el nombre del proceso: ")
    ProcessSize = input("Ingrese el tamaño de la particion: ")
    ProcessSize=int(ProcessSize)
    ProcessInputDict={"Nombre":ProcessName,"Tamaño":ProcessSize}
    WaitingList.append(ProcessInputDict)

    PartitionAvailable=CheckSize(CheckAvailability(AvailabilityList), PartitionList, ProcessSize)

    if PartitionAvailable == None:
        print("El proceso queda a la espera de una particion libre")
    else:
        MemoryProcessCount.append(True)
        PrincipalMemory[PartitionAvailable]= WaitingList.pop()
        AvailabilityList[PartitionAvailable] = False

        nuevoingreso=input("Deseas Ingresar otra instruccion (Y/N): ")

        if nuevoingreso == "Y":
            ProcessInput(AvailabilityList,PartitionList)
        elif nuevoingreso =="N":
            print("Volviendo al ménu")




def RemoveProcess():

    if len(CheckAvailability())>0:
        ProcessNumber=input("Seleccione el numero de proceso que desea sacar (Opcioned validas (1-7)")

        FinishedProcesses.append(PrincipalMemory[ProcessNumber])
        PrincipalMemory[ProcessNumber]=None
        AvailabilityList[ProcessNumber]=True


    else:
        print("No hay procesos en cola para remover")


def FinishProgram():
    print(f'Se cargaron {len(MemoryProcessCount)} en memoria principal')
    print(f'Se terminaron {len(FinishedProcesses)} procesos antes de terminar la simulacion')
    print(f'La Cantidad de procesos que quedaron sin ser ejecutados son  {len(WaitingList)} en memoria principal')



def ShowWaitinListProcesses():
    return print(WaitingList)








main_menu()













