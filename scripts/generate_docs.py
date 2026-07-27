# -*- coding: utf-8 -*-
"""
Genera el documento PDF con la documentación interna de Modova
(tienda online de ropa), usado como fuente de conocimiento del agente RAG.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, ListFlowable, ListItem
)

OUTPUT_PATH = "Modova_Documentacion_Interna.pdf"

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="H1Custom", parent=styles["Heading1"],
                           spaceAfter=14, textColor="#1a1a2e"))
styles.add(ParagraphStyle(name="H2Custom", parent=styles["Heading2"],
                           spaceBefore=10, spaceAfter=8, textColor="#16213e"))
styles.add(ParagraphStyle(name="BodyCustom", parent=styles["Normal"],
                           fontSize=10.5, leading=15, alignment=TA_LEFT,
                           spaceAfter=8))

story = []

def h1(text):
    story.append(Paragraph(text, styles["H1Custom"]))

def h2(text):
    story.append(Paragraph(text, styles["H2Custom"]))

def p(text):
    story.append(Paragraph(text, styles["BodyCustom"]))

def bullets(items):
    story.append(ListFlowable(
        [ListItem(Paragraph(i, styles["BodyCustom"])) for i in items],
        bulletType="bullet", start="•"
    ))
    story.append(Spacer(1, 8))

# ---------------------------------------------------------------------------
# PORTADA
# ---------------------------------------------------------------------------
story.append(Spacer(1, 6*cm))
story.append(Paragraph("MODOVA", ParagraphStyle(
    name="Title", parent=styles["Title"], fontSize=32, textColor="#1a1a2e")))
story.append(Paragraph("Documentación Interna — Tienda Online de Ropa",
                        ParagraphStyle(name="Subtitle", parent=styles["Normal"],
                                       fontSize=14, textColor="#555555",
                                       spaceBefore=10)))
story.append(Spacer(1, 1*cm))
p("Este documento reúne las políticas y procesos oficiales de Modova: "
  "privacidad, reembolsos y devoluciones, preguntas frecuentes, envíos y "
  "entregas, y términos y condiciones. Es utilizado como base de "
  "conocimiento para el agente de atención al cliente impulsado por IA.")
story.append(PageBreak())

# ---------------------------------------------------------------------------
# 1. POLÍTICA DE PRIVACIDAD
# ---------------------------------------------------------------------------
h1("1. Política de Privacidad")

h2("1.1 Datos que recopilamos")
p("Modova recopila los siguientes datos personales cuando el cliente crea "
  "una cuenta, realiza una compra o se suscribe a nuestro boletín: nombre "
  "completo, correo electrónico, número de teléfono, dirección de envío, "
  "talla preferida y datos de pago (procesados de forma segura por nuestra "
  "pasarela de pagos, nunca almacenados directamente en nuestros servidores).")

h2("1.2 Uso de los datos")
bullets([
    "Procesar y enviar los pedidos realizados en la tienda.",
    "Enviar notificaciones sobre el estado del pedido (confirmación, envío, entrega).",
    "Personalizar recomendaciones de productos según el historial de compras.",
    "Enviar promociones y novedades, solo si el cliente aceptó recibir comunicaciones de marketing.",
    "Cumplir con obligaciones legales y fiscales.",
])

h2("1.3 Conservación de los datos")
p("Los datos de la cuenta se conservan mientras el cliente mantenga su "
  "cuenta activa. Si el cliente solicita la eliminación de su cuenta, los "
  "datos personales se eliminan en un plazo máximo de 30 días hábiles, "
  "excepto la información que debamos conservar por obligación legal "
  "(por ejemplo, facturas, durante 5 años).")

h2("1.4 Derechos del cliente")
p("El cliente puede solicitar en cualquier momento el acceso, "
  "rectificación, eliminación u oposición al tratamiento de sus datos "
  "personales escribiendo a privacidad@modova.com. Modova responderá a "
  "la solicitud en un plazo máximo de 15 días hábiles.")

h2("1.5 Cookies")
p("El sitio web de Modova utiliza cookies propias y de terceros para "
  "mejorar la experiencia de navegación, recordar el contenido del "
  "carrito de compras y analizar el tráfico del sitio. El cliente puede "
  "desactivar las cookies desde la configuración de su navegador, aunque "
  "esto puede afectar el funcionamiento del carrito de compras.")

story.append(PageBreak())

# ---------------------------------------------------------------------------
# 2. POLÍTICA DE REEMBOLSOS Y DEVOLUCIONES
# ---------------------------------------------------------------------------
h1("2. Política de Reembolsos y Devoluciones")

h2("2.1 Plazo para devoluciones")
p("El cliente dispone de 30 días calendario desde la fecha de entrega "
  "para solicitar la devolución de un producto, siempre que se cumplan "
  "las condiciones descritas a continuación.")

h2("2.2 Condiciones del producto")
bullets([
    "El producto debe estar sin usar, sin lavar y con las etiquetas originales.",
    "Debe devolverse en su empaque original o uno similar que lo proteja adecuadamente.",
    "No se aceptan devoluciones de ropa interior, trajes de baño ni accesorios personales por razones de higiene, salvo defecto de fábrica.",
    "Los artículos en oferta o liquidación final no son reembolsables, solo se permite cambio de talla, sujeto a disponibilidad.",
])

h2("2.3 Proceso de devolución")
p("Para iniciar una devolución, el cliente debe ingresar a “Mis pedidos” "
  "en su cuenta de Modova, seleccionar el producto y elegir el motivo de "
  "la devolución. Modova generará una guía de envío gratuita para "
  "devoluciones dentro del país. El paquete debe entregarse a la "
  "transportadora dentro de los 7 días siguientes a la generación de la guía.")

h2("2.4 Tiempos de reembolso")
p("Una vez que el equipo de calidad de Modova recibe e inspecciona el "
  "producto devuelto (proceso que toma entre 2 y 4 días hábiles), el "
  "reembolso se procesa al mismo método de pago original en un plazo de "
  "5 a 10 días hábiles adicionales, dependiendo de la entidad bancaria.")

h2("2.5 Productos defectuosos o con error de envío")
p("Si el cliente recibe un producto defectuoso, dañado o diferente al "
  "solicitado, Modova cubre el 100% del costo de devolución y ofrece, a "
  "elección del cliente, reembolso total o reemplazo inmediato del "
  "artículo, sin necesidad de esperar la inspección del producto devuelto.")

story.append(PageBreak())

# ---------------------------------------------------------------------------
# 3. PREGUNTAS FRECUENTES (FAQ)
# ---------------------------------------------------------------------------
h1("3. Preguntas Frecuentes (FAQ)")

h2("¿Cómo sé qué talla elegir?")
p("Cada producto cuenta con una guía de tallas específica en su página, "
  "ya que las medidas pueden variar según la marca y el tipo de prenda. "
  "Recomendamos comparar tus medidas corporales con la tabla de tallas "
  "antes de comprar.")

h2("¿Modova tiene tiendas físicas?")
p("No. Modova opera exclusivamente como tienda online, lo que nos "
  "permite ofrecer precios más competitivos y un catálogo más amplio "
  "que una tienda física tradicional.")

h2("¿Puedo modificar o cancelar mi pedido después de confirmarlo?")
p("Los pedidos pueden modificarse o cancelarse únicamente dentro de la "
  "primera hora después de la compra, escribiendo a soporte@modova.com "
  "o mediante el chat de atención al cliente. Pasado ese tiempo, el "
  "pedido entra en preparación y no puede modificarse.")

h2("¿Qué métodos de pago acepta Modova?")
p("Aceptamos tarjetas de crédito y débito (Visa, Mastercard, American "
  "Express), PayPal, y pago contra entrega disponible únicamente en "
  "ciudades principales.")

h2("¿Ofrecen descuentos para nuevos clientes?")
p("Sí, los nuevos clientes reciben un 10% de descuento en su primera "
  "compra al suscribirse al boletín de Modova con su correo electrónico.")

h2("¿Cómo contacto al servicio de atención al cliente?")
p("Puedes escribirnos a soporte@modova.com, a través del chat en vivo "
  "en nuestro sitio web (disponible de lunes a sábado, 8:00 a.m. a "
  "8:00 p.m.), o por WhatsApp al número que aparece en el pie de página "
  "del sitio.")

story.append(PageBreak())

# ---------------------------------------------------------------------------
# 4. GUÍA DE ENVÍOS Y ENTREGAS
# ---------------------------------------------------------------------------
h1("4. Guía de Envíos y Entregas")

h2("4.1 Tiempos de entrega")
bullets([
    "Ciudades principales: 2 a 4 días hábiles.",
    "Ciudades intermedias: 4 a 6 días hábiles.",
    "Zonas rurales o de difícil acceso: 6 a 10 días hábiles.",
    "Envíos internacionales (disponibles a países seleccionados): 8 a 15 días hábiles.",
])

h2("4.2 Costos de envío")
p("El envío estándar dentro del país tiene un costo fijo, pero es "
  "gratuito en compras superiores a $80.000 (o el equivalente en la "
  "moneda local configurada en el sitio). El envío express, con entrega "
  "en 24 a 48 horas en ciudades principales, tiene un costo adicional "
  "que se calcula al finalizar la compra.")

h2("4.3 Seguimiento del pedido")
p("Una vez despachado el pedido, el cliente recibe un correo electrónico "
  "con el número de guía y un enlace para rastrear el envío en tiempo "
  "real. El estado del pedido también puede consultarse desde la sección "
  "“Mis pedidos” en la cuenta de Modova.")

h2("4.4 Pedidos no entregados")
p("Si la transportadora no logra entregar el pedido tras 3 intentos, el "
  "paquete es devuelto automáticamente al centro de distribución de "
  "Modova. El cliente será contactado para coordinar un nuevo envío "
  "(con costo adicional) o el reembolso del valor de los productos, "
  "descontando el costo de envío inicial si este fue gratuito.")

story.append(PageBreak())

# ---------------------------------------------------------------------------
# 5. TÉRMINOS Y CONDICIONES
# ---------------------------------------------------------------------------
h1("5. Términos y Condiciones")

h2("5.1 Aceptación de los términos")
p("Al crear una cuenta o realizar una compra en Modova, el cliente "
  "acepta los presentes términos y condiciones, así como la política de "
  "privacidad y la política de reembolsos y devoluciones.")

h2("5.2 Disponibilidad de productos")
p("Todos los productos están sujetos a disponibilidad de inventario. "
  "Modova se reserva el derecho de cancelar pedidos de productos que se "
  "muestren erróneamente como disponibles debido a fallas técnicas, "
  "notificando al cliente y reembolsando el valor pagado en su totalidad.")

h2("5.3 Precios y promociones")
p("Los precios publicados incluyen impuestos aplicables, salvo que se "
  "indique lo contrario. Modova puede modificar precios y promociones "
  "sin previo aviso, sin que esto afecte los pedidos ya confirmados.")

h2("5.4 Propiedad intelectual")
p("Todo el contenido del sitio web de Modova (imágenes, textos, logotipos "
  "y diseño) es propiedad de Modova o de sus licenciantes y está "
  "protegido por las leyes de propiedad intelectual. Queda prohibida su "
  "reproducción total o parcial sin autorización expresa.")

h2("5.5 Programa de fidelidad “Modova Club”")
p("Los clientes registrados acumulan puntos equivalentes al 5% del valor "
  "de cada compra, que pueden canjearse por descuentos en compras "
  "futuras. Los puntos son válidos durante 12 meses desde su acumulación "
  "y no son transferibles ni canjeables por dinero en efectivo.")

h2("5.6 Ley aplicable y resolución de disputas")
p("Estos términos se rigen por las leyes del país de operación de "
  "Modova. Cualquier disputa relacionada con la compra de productos se "
  "intentará resolver primero de manera directa a través del servicio "
  "de atención al cliente antes de recurrir a instancias legales.")

doc = SimpleDocTemplate(OUTPUT_PATH, pagesize=letter,
                         topMargin=2*cm, bottomMargin=2*cm,
                         leftMargin=2*cm, rightMargin=2*cm)
doc.build(story)
print(f"PDF generado: {OUTPUT_PATH}")
