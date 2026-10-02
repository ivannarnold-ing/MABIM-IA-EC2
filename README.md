# MABIM-IA-EC2
Archivo de QA/QC en Dynamo y Python que audita la asignación del parámetro "Código de montaje" en elementos estructurales de Revit frente a un estándar definido. Genera un reporte detallado y lo exporta automáticamente a Excel con el ID de cada elemento para facilitar su corrección en el modelo.

# EVALUACIÓN CONTINUA 2 - EC2, INTEGRANTES:
- Ivann Arnold Maldonado Huancachoque
- Ivan Guillen Challco



1. ¿Qué hace la rutina?
Es una rutina de control de calidad (QA/QC) orientada a la verificación de modelos BIM en Revit. Inspecciona de forma automatizada los elementos de una categoría seleccionada (ejemplares y tipos) para comprobar si cuentan con el parámetro de clasificación de partidas (Código de montaje / Assembly Code) debidamente asignado y alineado al estándar del proyecto, previniendo errores u omisiones en etapas de metrados y presupuestos.  

2. ¿Qué recibe la rutina? (Entradas / IN)
- IN[0] (Elementos): La lista de instancias de Revit recolectadas desde el nodo All Elements of Category a partir de una categoría específica (por ejemplo, Armazón estructural o Pilares estructurales).   
- IN[1] (Valores de estándar - Opcional): Una lista de códigos válidos o nomenclaturas autorizadas (ej. ["STR-COL-01", "STR-COL-02", ...]) contra las cuales se contrasta el parámetro auditado.   
- Contexto de Revit (doc): El documento activo de Revit mediante DocumentManager para acceder a la base de datos de tipos y familias (GetTypeId). 
  
3. ¿Qué produce la rutina? (Salidas / OUT)
- OUT (Matriz tabular): Una lista bidimensional (filas y columnas) que contiene una fila de encabezados seguida de los registros auditados:   
    - ID Elemento: Identificador numérico único de Revit para localizar y aislar rápidamente el elemento en el modelo.   
    - Tipo / Familia: Nombre de la tipología o símbolo asignado al elemento.
    - Nivel: Nivel o restricción de referencia donde se ubica el elemento en el proyecto.   
    - Código Asignado: Valor leído del parámetro Código de montaje / Assembly Code (o "Vacío" si no tiene asignación).
    - Estado QA/QC: Diagnóstico de cumplimiento clasificado en:
        - OK (cumple el estándar).   
        - Sin Asignar (parámetro existente pero en blanco).
        - Código Fuera de Estándar (código presente pero no reconocido en la lista oficial).   
        - Falta Parámetro (parámetro no cargado en el ejemplar ni en el tipo).   Reporte en Hoja de  
- Cálculo (.xlsx): A través del nodo Data.OpenXMLExportExcel, genera físicamente un archivo Excel en la ruta designada con el consolidado de la auditoría para su revisión por parte del equipo de modelado o coordinación. 