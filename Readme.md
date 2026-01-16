# DSL Framework de Integración

Este es un framework ligero de integración empresarial (EIP - Enterprise Integration Patterns) implementado en Java. Permite construir flujos de procesamiento de mensajes XML mediante la orquestación de componentes desacoplados.

## Características Principales

* **Orientado a Mensajes:** Todo el flujo de datos se realiza mediante objetos `Message` que encapsulan documentos XML (DOM) y cabeceras de metadatos.
* **Arquitectura de Pipe-and-Filter:** Los componentes (`Tasks`) se conectan a través de canales (`Slots`) y puertos (`Ports`).
* **Soporte de Patrones EIP:**
  * **Routing:** Router, Splitter, Merger, Filter, Distributor, Replicator, Correlator.
  * **Transformation:** Translator (XSLT), Aggregator.
  * **Modification:** Enricher, Slimmer.
* **Conectores:** Abstracción para interactuar con sistemas externos (Archivos, Consola, Bases de Datos, HTTP, colas simuladas).
* **Ejecución Flexible:** Soporta ejecución secuencial (single-threaded) y concurrente (thread-pool) con diferentes políticas de ejecución en cada `Flow`.

## Componentes del Core

### Elementos Básicos

* **Element:** Clase base con identificador único.
* **Slot:** Canal de comunicación asíncrono (Queue) entre componentes. Implementa el patrón Observer.
* **Message:** Envase de datos que viaja por los Slots. Contiene un `org.w3c.dom.Document` y un mapa de headers.

### Puertos

* **InputPort:** Recibe datos desde un Connector y los introduce al flujo.
* **OutputPort:** Extrae datos del flujo para entregarlos a un Connector.
* **RequestPort:** Puerto bidireccional para operaciones síncronas (Request-Reply).

### Tareas (Tasks)

Las tareas son las unidades de procesamiento.

* **Routers:** Dirigen el tráfico (e.g., `Distributor` envía a una salida basada en XPath).
* **Transformers:** Modifican la estructura del payload (e.g., `Translator` aplica XSLT).
* **Modifiers:** Alteran contenido puntual o metadatos (e.g., `CorrelationIdSetter`).

### Conectores

* **FileConnector:** Lectura/Escritura de archivos locales. Soporta directorios.
* **DataBaseConnector:** Ejecución de queries SQL dinámicas definidas en XML.
* **ConsoleConnector:** Salida a System.out para debugging.
* **HttpConnector:** Cliente HTTP básico.

## Ejemplo de Uso

```java
// 1. Definir Slots (Canales)
Slot inputSlot = new Slot("input");
Slot processSlot = new Slot("process");
Slot outputSlot = new Slot("output");

// 2. Configurar Conectores y Puertos
InputPort iPort = new InputPort(inputSlot);
FileConnector reader = new FileConnector(iPort, "C:/in/data.xml");

OutputPort oPort = new OutputPort("out-port", outputSlot);
ConsoleConnector writer = new ConsoleConnector(oPort);

// 3. Configurar Tarea (Ej. Transformación XSLT)
Translator translator = new Translator("my-translator", inputSlot, outputSlot, "/templates/convert.xslt");

// 4. Construir y Ejecutar el Flujo
Flow flow = new Flow.Builder("MainFlow")
    .concurrent(new FifoPolicy()) // Llamas a concurrent pasándole una política si quieres que sea concurrente
    .build();

flow.addElement(reader);
flow.addElement(translator);
flow.addElement(writer);

flow.execute();
```

## Requisitos

* Java 11+
* Maven 3.6+

## Compilación

### Ubicarse en la carpeta del proyecto:

```bash
cd dsl-framework
```

### Compilar proyecto

```bash
mvn clean install
```

### Compilar sin ejecutar tests

```bash
mvn clean install -DskipTests
```