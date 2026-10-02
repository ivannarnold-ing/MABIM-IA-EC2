import clr

# 1. Carga de ensamblados
clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

clr.AddReference('RevitNodes')
import Revit
clr.ImportExtensions(Revit.Elements)

doc = DocumentManager.Instance.CurrentDBDocument

elementos_in = IN[0] if isinstance(IN[0], list) else [IN[0]]

# Lista de códigos válidos esperados en el proyecto
if len(IN) > 1 and IN[1]:
    valores_validos = IN[1] if isinstance(IN[1], list) else [IN[1]]
else:
    valores_validos = ["STR-COL-01", "STR-COL-02", "STR-VIG-01", "STR-VIG-02", "03.01.01", "03.01.02"]

registros = []

for item in elementos_in:
    if item is None:
        continue

    # Desempaquetar elemento nativo si viene envuelto por Dynamo
    el = item.InternalElement if hasattr(item, "InternalElement") else item

    # A. ID del Elemento
    if hasattr(el, "Id"):
        el_id = el.Id.IntegerValue if hasattr(el.Id, "IntegerValue") else int(el.Id.Value)
    else:
        el_id = getattr(item, "Id", "S/N")

    # B. Nombre del Tipo / Familia (Método universal compatible con IronPython y CPython)
    nombre_tipo = "Sin Tipo"
    tipo_elem = None
    try:
        type_id = el.GetTypeId()
        if type_id and type_id != ElementId.InvalidElementId:
            tipo_elem = doc.GetElement(type_id)
            if tipo_elem:
                # 1. Intento por parámetro de sistema de nombre de tipo
                p_tipo = tipo_elem.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM)
                if p_tipo and p_tipo.AsString():
                    nombre_tipo = p_tipo.AsString()
                else:
                    # 2. Descriptores nativos según motor Python
                    try:
                        nombre_tipo = Element.Name.__get__(tipo_elem)
                    except:
                        nombre_tipo = tipo_elem.Name
    except:
        nombre_tipo = getattr(item, "Name", "Desconocido")

    # C. Nivel / Restricción de referencia
    param_nivel = (el.LookupParameter("Nivel de referencia") or 
                   el.LookupParameter("Restricción base") or 
                   el.LookupParameter("Nivel"))
    
    nivel_str = param_nivel.AsValueString() if (param_nivel and param_nivel.HasValue) else "Sin Nivel"

    # D. Parámetro auditado: Código de montaje (Assembly Code)
    param_codigo = el.LookupParameter("Código de montaje") or el.LookupParameter("Assembly Code")
    if (param_codigo is None or not param_codigo.HasValue) and tipo_elem:
        param_codigo = tipo_elem.LookupParameter("Código de montaje") or tipo_elem.LookupParameter("Assembly Code")

    # E. Lógica de validación QA/QC
    if param_codigo is None:
        codigo_val = "N/A"
        estado = "Falta Parámetro"
    elif not param_codigo.HasValue:
        codigo_val = "Vacío"
        estado = "Sin Asignar"
    else:
        codigo_val = param_codigo.AsString() or param_codigo.AsValueString() or ""
        codigo_val = codigo_val.strip()
        if codigo_val == "":
            codigo_val = "Vacío"
            estado = "Sin Asignar"
        elif codigo_val not in valores_validos:
            estado = "Código Fuera de Estándar"
        else:
            estado = "OK"

    registros.append([el_id, nombre_tipo, nivel_str, codigo_val, estado])

# Encabezados de salida
encabezados = ["ID Elemento", "Tipo / Familia", "Nivel", "Código Asignado", "Estado QA/QC"]
OUT = [encabezados] + registros