/*
  Archivo de prueba diseñado para validar los aportes de Diego Alfonzo.
  Debe validar correctamente:
  - Mapas asociativos
  - Operadores relacionales (==, !=, <, >, <=, >=)
  - Operadores lógicos (&&, ||, !)
  - Comentarios
  - Delimitadores
  - Literales de cadena y decimales
  - Funciones con retorno múltiple
  - Bucles for
*/
package main

import "fmt"

// Función con retorno múltiple
func dividir(a int, b int) (int, error) {
    if b == 0 {
        return 0, nil
    }
    return a / b, nil
}

func main() {
    // Declaración y asignación de un mapa asociativo (Clave string, Valor int)
    edades := map[string]int{"Diego": 21, "Arianna": 20, "Matias": 22}

    // Declaración y asignación de un mapa asociativo (Clave string, Valor float64)
    precios := map[string]float64{"manzana": 1.99, "banana": 0.85}

    // Operadores lógicos y relacionales
    x := 10.5
    y := 20.0

    if x < y && y >= 15.0 {
        fmt.Println("Cumple condicion logica")
    }

    if x == 10.5 || y != 20.0 {
        fmt.Println("Otra condicion")
    }

    noValido := !false

    // Impresión usando delimitadores
    fmt.Println(edades["Diego"], precios["manzana"], noValido)

    // Bucle for clásico
    var limite int = 10
    var divisor int = 2

    for i := 0; i < limite; i++ {
        res, _ := dividir(i, divisor)
        fmt.Println("Division de", i, "entre", divisor, "es", res)
    }
    edades2 := map[string]int{"Diego": 21}
    fmt.Println(edades2["Diego"])

    // Solicitud de datos
    var entrada string
    fmt.Scanln(&entrada)
    // Errores sencillos (caracteres no reconocidos)
    @
    $
    #

    // Errores más complejos (cadenas sin cerrar)
    cadenaIncompleta := "Esta cadena de texto nunca se cierra
    
    cadenaRawIncompleta := `Esta cadena tampoco se cierra
}

/* Comentario se queda abierto al final del archivo

