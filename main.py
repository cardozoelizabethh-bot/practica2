import flet as ft

# 1. DATOS
precio_procesador = {"Core i3": 300000, "Core i5": 600000, "Core i7": 1000000}
watts_procesador = {"Core i3": 65, "Core i5": 95, "Core i7": 125}
opciones_ram = [8, 16, 32, 64]
precio_ram = {8: 40000, 16: 70000, 32: 130000, 64: 250000}

precio_GPU = 400000
watts_GPU = 150
precio_SSD = 60000
precio_armado = 30000
costo_envio = 15000
watts_base_sistema = 100


def main(page: ft.Page):
    page.title = "Cotizador de informática"
    page.scroll = ft.ScrollMode.AUTO

    # 2. DECLARACION DE COMPONENTES
    nombre = ft.TextField(label="Nombre del cliente", width=320)
    presupuesto = ft.TextField(label="Presupuesto tope (en pesos)", width=320)

    dd_procesador = ft.Dropdown(
        label="Procesador",
        width=320,
        options=[ft.dropdown.Option(proc) for proc in precio_procesador],
    )

    ram_actual = ft.Text("Memoria RAM: 8 GB")
    sld_ram = ft.Slider(min=0, max=3, divisions=3, value=0, width=320, on_change=lambda e: actualizar_ram())

    gpu = ft.Checkbox(label="Placa de video dedicada")
    unidad_SSD = ft.Checkbox(label="Unidad SSD extra")
    armado = ft.Checkbox(label="Servicio de armado")

    # Apagado = retiro en tienda / Encendido = envío a domicilio
    envio = ft.Switch(label="Activar para envío a domicilio (apagado para retiro en tienda)")

    grupo_radios = ft.RadioGroup(
        value="Efectivo",
        content=ft.Column([
            ft.Radio(value="Efectivo", label="Efectivo o Transferencia bancaria (10% descuento)"),
            ft.Radio(value="Débito", label="Tarjeta de Débito (precio de lista)"),
            ft.Radio(value="Crédito", label="Tarjeta de Crédito en 3 cuotas (15% recargo)"),
        ]),
    )

    # Resultados
    txt_alerta = ft.Text("", color=ft.Colors.RED, weight=ft.FontWeight.BOLD)
    campo_subtotal = ft.Text("", size=16)
    campo_total = ft.Text("", size=16)
    campo_cuota = ft.Text("", size=16)
    campo_potencia = ft.Text("", size=16)
    campo_fuente = ft.Text("", size=16)
    txt_veredicto = ft.Text("", size=16, weight=ft.FontWeight.BOLD)

    # 3. FUNCIONES CONTROLADORAS DE EVENTOS
    def actualizar_ram():
        ram_actual.value = f"Memoria RAM: {opciones_ram[int(sld_ram.value)]} GB"
        page.update()

    def calcular(e):
        # Limpiar resultados anteriores
        txt_alerta.value = ""
        txt_veredicto.value = ""
        campo_subtotal.value = ""
        campo_total.value = ""
        campo_cuota.value = ""
        campo_potencia.value = ""
        campo_fuente.value = ""

        # Validar procesador y forma de pago
        if not dd_procesador.value or not grupo_radios.value:
            txt_alerta.value = "Seleccioná un procesador y una forma de pago."
            page.update()
            return

        # Leer presupuesto
        try:
            tope = float(presupuesto.value)
        except ValueError:
            txt_alerta.value = "El presupuesto debe ser un número."
            page.update()
            return

        # Subtotal
        gb = opciones_ram[int(sld_ram.value)]
        subtotal = precio_procesador[dd_procesador.value] + precio_ram[gb]
        if gpu.value:
            subtotal += precio_GPU
        if unidad_SSD.value:
            subtotal += precio_SSD
        if armado.value:
            subtotal += precio_armado
        if envio.value:
            subtotal += costo_envio

        # Medio de pago
        cuota = None
        if grupo_radios.value == "Efectivo":
            total = subtotal * 0.90
        elif grupo_radios.value == "Débito":
            total = subtotal
        else:
            total = subtotal * 1.15
            cuota = total / 3

        # Consumo y fuente
        watts = watts_procesador[dd_procesador.value] + watts_base_sistema
        if gpu.value:
            watts += watts_GPU
        watts = watts * 1.25

        if watts > 450:
            fuente = "Fuente de 650W o superior"
        else:
            fuente = "Fuente convencional de 500W"

        # Mostrar resultados
        campo_subtotal.value = f"Subtotal: $ {subtotal:,.2f}"
        campo_total.value = f"Total a pagar: ${total:,.2f}"
        campo_cuota.value = f"Valor de cada cuota: ${cuota:,.2f}" if cuota else "Valor de cada cuota: No aplica"
        campo_potencia.value = f"Consumo estimado: {watts:.1f} W"
        campo_fuente.value = f"Fuente recomendada: {fuente}"

        # Comparar con el presupuesto
        if total <= tope:
            txt_veredicto.value = f"Entra en el presupuesto. Saldo a favor: ${tope - total:,.2f}"
            txt_veredicto.color = ft.Colors.GREEN
        else:
            txt_veredicto.value = f"Excede el presupuesto. Faltan: ${total - tope:,.2f}"
            txt_veredicto.color = ft.Colors.RED
        page.update()

    boton_calcular = ft.Button("Calcular cotización", on_click=calcular)

    # 4. ENSAMBLADO FINAL
    page.add(
        nombre,
        presupuesto,
        dd_procesador,
        ram_actual,
        sld_ram,
        gpu,
        unidad_SSD,
        armado,
        envio,
        grupo_radios,
        boton_calcular,
        ft.Divider(),
        ft.Text("Resultados", size=20, weight=ft.FontWeight.BOLD),
        txt_alerta,
        campo_subtotal,
        campo_total,
        campo_cuota,
        campo_potencia,
        campo_fuente,
        txt_veredicto,
    )
ft.run(main)
