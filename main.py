import numpy
import pandas as pd

PartitionSize=pd.read_csv("Data/size.csv")
PartitionList= PartitionSize["Size"].values.tolist()
WaitingList=[]
AvailabilityList=[True,True,True,True,True,True,True]
PrincipalMemory=[None,None,None,None,None,None,None,None]
FinishedProcesses=[]

MemoryProcessCount=[]

TotalMemorySpace= sum(PartitionList)



def main_menu():
    print("Simulador de Ingreso de procesos en una memoria principal particionada")
    print("1. Imprimir proceso: ")
    print("2. Ingresar proceso: ")
    print("3. Mostrar cola de procesos en espera: ")
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
        ShowWaitinListProcesses(WaitingList)
    elif opcion == '4':
        RemoveProcess()

    elif opcion == '5':
        FinishProgram()
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

    SizeListDict = dict(zip(AvailableList, FilteredElements))

    MaxSizeAvailable=sum(FilteredElements)

    if ProcessSize>= MaxSizeAvailable:
        print("------------------------------------------------------------------------------------------------------------------------")
        print("Necesitas más espacio en memoria para introducir el proceso. Intenta eliminar uno o mas espacios para liberar la memoria")
        print("------------------------------------------------------------------------------------------------------------------------")

    if ProcessSize<=MaxSizeAvailable:

        SizeCombine=0
        AvailableMemorySpaceKeys=[]

        while ProcessSize> SizeCombine:
            min_key = min(SizeListDict, key=lambda k: SizeListDict[k])
            min_value = SizeListDict[min_key]
            AvailableMemorySpaceKeys.append(min_key)
            SizeCombine+=min_value
            del SizeListDict[min_key]

        return AvailableMemorySpaceKeys







def ProcessInput(AvailabilityList,PartitionList):

    ProcessName= input("Ingrese el nombre del proceso: ")
    ProcessSize = input("Ingrese el tamaño de la particion: ")
    ProcessSize=int(ProcessSize)
    ProcessInputDict={"Nombre":ProcessName,"Tamaño":ProcessSize}
    WaitingList.append(ProcessInputDict)

    PartitionAvailable=CheckSize(CheckAvailability(AvailabilityList), PartitionList, ProcessSize)
    if PartitionAvailable == None and ProcessSize >= TotalMemorySpace:
        print("El proceso exede el maximo de la memoria disponible")
        WaitingList.pop()

    elif PartitionAvailable == None:
        print("El proceso queda a la espera de una particion libre")
    else:
        MemoryProcessCount.append(True)
        WaitingTemp=WaitingList.pop()

        for PartitionKey in PartitionAvailable:
            PrincipalMemory[PartitionKey]=WaitingTemp
            AvailabilityList[PartitionKey]=False

        nuevoingreso=input("Si deseas Ingresar otra instruccion presiona Y de lo contrario presiona cualquier tecla para regresar al menu principal: ")

        if nuevoingreso == "Y" or nuevoingreso=="y":
            ProcessInput(AvailabilityList,PartitionList)
        else:
            print("Volviendo al ménu")
            main_menu()





def RemoveProcess():
    print(len(CheckAvailability(AvailabilityList)))


    if len(CheckAvailability(AvailabilityList))>0 and len(CheckAvailability(AvailabilityList))<=7:
        ProcessNumber=input("Seleccione el numero de proceso que desea sacar (Opcioned validas (1-7)")

        FinishedProcesses.append(PrincipalMemory[ProcessNumber])
        PrincipalMemory[ProcessNumber]=None
        AvailabilityList[ProcessNumber]=True



        nuevoingreso = input("Deseas remover otra instruccion (Y/N): ")

        if nuevoingreso == "Y" or nuevoingreso =="y":
            RemoveProcess()
        elif nuevoingreso == "N" or nuevoingreso=="n":
            print("Volviendo al ménu principal")

    else:
        print("-------------------------------------")
        print("No hay procesos en cola para remover")
        print("-------------------------------------")

        main_menu()


def FinishProgram():
    print("---------------------------------------------------------------")
    print("Se termino el programa")
    print(f'Se cargaron {len(MemoryProcessCount)} en memoria principal')
    print(f'Se terminaron {len(FinishedProcesses)} procesos antes de terminar la simulacion')
    print(f'La Cantidad de procesos que quedaron sin ser ejecutados son  {len(WaitingList)} en memoria principal')
    print("---------------------------------------------------------------")



def ShowWaitinListProcesses(WaitingList):

    if len(WaitingList)>0:
        print("---------------------------------------------------------------")
        print("Lista de procesos en espera para entrar en la memoria principal")
        print(WaitingList)
        print("---------------------------------------------------------------")
        main_menu()
    else:
        print("----------------------------------")
        print("No hay procesos en lista de espera")
        print("----------------------------------")
        main_menu()








main_menu()













